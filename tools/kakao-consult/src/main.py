"""Pipeline orchestrator -- wire all stages together."""

from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import dataclass
from pathlib import Path

from src.config import Settings, load_settings
from src.db.repository import Repository
from src.utils.logger import get_logger, setup_logging
from src.utils.time_utils import is_active_hours

logger = get_logger("main")


@dataclass
class PipelineRunResult:
    """Aggregated result from a full pipeline run."""

    messages_received: int = 0
    messages_responded: int = 0
    faq_matches: int = 0
    llm_responses: int = 0
    errors: int = 0
    success: bool = False
    error: str | None = None


@dataclass
class PipelineComponents:
    """Injectable pipeline dependencies for testability."""

    device_mgr: object  # DeviceManager
    monitor: object  # MessageMonitor
    navigator: object  # Navigator
    sender: object  # MessageSender
    classifier: object  # MessageClassifier
    router: object  # LLMRouter
    classify_pipeline: object  # ClassifyPipeline
    respond_pipeline: object  # RespondPipeline
    send_pipeline: object  # SendPipeline
    tracker: object  # ActionTracker
    limiter: object  # CompositeRateLimiter


class PipelineRunner:
    """Orchestrate the Monitor -> Classify -> Respond -> Send pipeline."""

    def __init__(
        self,
        settings: Settings,
        repository: Repository,
        components: PipelineComponents | None = None,
    ) -> None:
        self._settings = settings
        self._repo = repository
        self._initialized = False
        self._device: object | None = None
        if components is not None:
            self._inject_components(components)

    def _inject_components(self, c: PipelineComponents) -> None:
        """Install pre-built components (for testing)."""
        self._device_mgr = c.device_mgr
        self._device = None
        self._monitor = c.monitor
        self._navigator = c.navigator
        self._sender = c.sender
        self._classify = c.classify_pipeline
        self._respond = c.respond_pipeline
        self._send = c.send_pipeline
        self._tracker = c.tracker
        self._limiter = c.limiter
        self._initialized = True

    def _lazy_init(self) -> None:
        """Lazy initialization of components that need external deps."""
        if self._initialized:
            return

        from src.ai.classifier import MessageClassifier
        from src.ai.providers.claude import ClaudeProvider
        from src.ai.providers.ollama import OllamaProvider
        from src.ai.providers.openai_provider import OpenAIProvider
        from src.ai.router import LLMRouter
        from src.emulator.device import DeviceManager
        from src.kakao.monitor import MessageMonitor
        from src.kakao.navigator import Navigator
        from src.kakao.sender import MessageSender
        from src.knowledge.faq_matcher import FAQMatcher
        from src.knowledge.templates import TemplateEngine
        from src.pipeline.classify import ClassifyPipeline
        from src.pipeline.respond import RespondPipeline
        from src.pipeline.send import SendPipeline
        from src.pipeline.track import ActionTracker
        from src.utils.rate_limiter import CompositeRateLimiter

        s = self._settings
        project_root = Path(__file__).resolve().parent.parent

        # Device
        self._device_mgr = DeviceManager(serial=s.emulator.serial)

        # KakaoTalk UI
        device = self._device_mgr.connect()
        self._device = device
        self._monitor = MessageMonitor(device, s.monitor.ignored_chatrooms)
        self._navigator = Navigator(device)
        self._sender = MessageSender(
            device,
            typing_delay_per_char_ms=s.response.typing_delay_per_char_ms,
            min_delay=s.response.min_response_delay_seconds,
            max_delay=s.response.max_response_delay_seconds,
        )

        # Templates
        templates_dir = project_root / s.template.templates_dir
        self._template_engine = TemplateEngine(templates_dir)
        self._template_engine.load()
        self._faq_matcher = FAQMatcher(templates_dir, s.template.fuzzy_threshold)
        self._faq_matcher.load()

        # AI
        self._classifier = MessageClassifier(
            api_key=s.anthropic_api_key,
            model=s.classifier.model,
            confidence_threshold=s.classifier.confidence_threshold,
        )

        providers = {}
        if s.anthropic_api_key:
            providers["claude"] = ClaudeProvider(
                api_key=s.anthropic_api_key,
                model=s.llm.claude_model,
                max_tokens=s.llm.max_tokens,
                temperature=s.llm.temperature,
            )
        if s.openai_api_key:
            providers["openai"] = OpenAIProvider(
                api_key=s.openai_api_key,
                model=s.llm.openai_model,
                max_tokens=s.llm.max_tokens,
                temperature=s.llm.temperature,
            )
        providers["ollama"] = OllamaProvider(
            base_url=s.llm.ollama_base_url,
            model=s.llm.ollama_model,
            max_tokens=s.llm.max_tokens,
            temperature=s.llm.temperature,
        )

        self._router = LLMRouter(providers, s.llm.default_provider)

        # Pipelines
        self._classify = ClassifyPipeline(
            self._faq_matcher, self._classifier, s.classifier.use_local_first
        )
        self._respond = RespondPipeline(self._template_engine, self._router)
        self._send = SendPipeline(self._sender)
        self._tracker = ActionTracker(self._repo)

        # Rate limiter
        self._limiter = CompositeRateLimiter(
            hourly_limit=s.rate_limit.max_responses_per_hour,
            daily_limit=s.rate_limit.max_responses_per_day,
            min_interval_seconds=s.rate_limit.min_interval_seconds,
        )

        self._initialized = True

    async def run_once(self, *, dry_run: bool = False) -> PipelineRunResult:
        """Execute a single polling cycle."""
        result = PipelineRunResult()

        try:
            self._lazy_init()

            # Reconnect device if connection lost
            try:
                self._device = self._device_mgr.ensure_connected()
                # Update device reference in components
                self._monitor._device = self._device
                self._navigator._device = self._device
                self._sender._device = self._device
            except ConnectionError as exc:
                logger.error("device_reconnect_failed", error=str(exc))
                result.error = f"Device connection lost: {exc}"
                return result

            # Check active hours
            if not is_active_hours(
                self._settings.scheduling.active_start_hour,
                self._settings.scheduling.active_end_hour,
            ):
                logger.info("outside_active_hours")
                result.success = True
                return result

            # Ensure KakaoTalk is in foreground and on chat list
            self._navigator.ensure_kakao_foreground()
            if not self._navigator.is_in_chat_list():
                self._navigator.go_to_chat_list()

            # Poll for new messages
            new_messages = self._monitor.poll()
            result.messages_received = len(new_messages)

            if not new_messages:
                result.success = True
                return result

            for msg in new_messages:
                try:
                    # Rate limit check
                    can_respond = await self._limiter.can_respond(msg.chatroom_id)
                    if not can_respond:
                        logger.info("rate_limited", chatroom=msg.chatroom_id)
                        continue

                    # Check blocked users
                    if self._repo.is_user_blocked(msg.sender):
                        logger.info("user_blocked", sender=msg.sender)
                        continue

                    # Record incoming message
                    self._tracker.record_receive(msg.chatroom_id, msg.text)
                    self._repo.upsert_conversation(
                        msg.chatroom_id, msg.chatroom_name, msg.sender
                    )
                    self._repo.insert_message(msg.chatroom_id, "incoming", msg.text)

                    # Classify
                    classify_result = await self._classify.run(msg.text)

                    # Get conversation history for LLM context
                    history: list[dict[str, str]] = []
                    if not classify_result.used_local:
                        raw_history = self._repo.get_conversation_history(
                            msg.chatroom_id, limit=10
                        )
                        for h in reversed(raw_history):
                            role = (
                                "user" if h["direction"] == "incoming" else "assistant"
                            )
                            history.append({"role": role, "content": h["content"]})

                    # Generate response
                    respond_result = await self._respond.run(
                        msg.text, classify_result, history
                    )

                    # Skip empty responses (spam)
                    if not respond_result.text:
                        continue

                    if not dry_run:
                        # Navigate to chatroom
                        self._navigator.enter_chatroom(msg.chatroom_name)

                        # Send response
                        send_result = await self._send.run(
                            msg.chatroom_id,
                            respond_result.text,
                            self._settings.response.max_response_length,
                        )

                        # Navigate back to chat list
                        self._navigator.go_to_chat_list()

                        if send_result.success:
                            result.messages_responded += 1
                            await self._limiter.record_response(msg.chatroom_id)
                    else:
                        logger.info(
                            "dry_run_skip_send",
                            chatroom=msg.chatroom_id,
                            response_preview=respond_result.text[:50],
                        )
                        result.messages_responded += 1

                    # Track
                    self._tracker.record_respond(
                        msg.chatroom_id,
                        respond_result.provider,
                        respond_result.classification,
                    )
                    self._repo.insert_message(
                        msg.chatroom_id,
                        "outgoing",
                        respond_result.text,
                        classification=respond_result.classification,
                        confidence=respond_result.confidence,
                        llm_provider=respond_result.provider,
                        template_id=respond_result.template_id,
                    )

                    if respond_result.provider == "template":
                        result.faq_matches += 1
                    else:
                        result.llm_responses += 1

                except Exception as exc:
                    result.errors += 1
                    self._tracker.record_error(
                        "message_processing", str(exc), msg.chatroom_id
                    )
                    logger.error(
                        "message_error", chatroom=msg.chatroom_id, error=str(exc)
                    )

            result.success = True
            self._tracker.log_summary()

        except Exception as exc:
            result.error = str(exc)
            logger.error("pipeline_error", error=str(exc))

        return result


def _verify_startup(settings: Settings) -> list[str]:
    """Verify required resources."""
    errors: list[str] = []
    if not settings.anthropic_api_key:
        errors.append("ANTHROPIC_API_KEY is not set")
    return errors


async def _async_main(args: argparse.Namespace) -> int:
    settings = load_settings()
    setup_logging(level=settings.logging.level, log_dir=settings.logging.log_dir)
    logger.info("pipeline_starting", mode="dry_run" if args.dry_run else "live")

    if not args.dry_run:
        errors = _verify_startup(settings)
        if errors:
            for err in errors:
                logger.error("startup_check_failed", error=err)
            return 1

    repo = Repository(settings.database.path)
    repo.init_db()

    runner = PipelineRunner(settings, repo)

    if args.once:
        result = await runner.run_once(dry_run=args.dry_run)
        if result.success:
            logger.info(
                "pipeline_complete",
                received=result.messages_received,
                responded=result.messages_responded,
                faq=result.faq_matches,
                llm=result.llm_responses,
                errors=result.errors,
            )
            return 0
        logger.error("pipeline_failed", error=result.error)
        return 1

    # Scheduled mode
    from apscheduler.schedulers.asyncio import AsyncIOScheduler

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        runner.run_once,
        "interval",
        seconds=settings.monitor.poll_interval_seconds,
    )
    scheduler.start()
    logger.info(
        "scheduler_started", interval=settings.monitor.poll_interval_seconds
    )

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("scheduler_stopped")

    repo.close()
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="KakaoTalk Consultation Bot")
    parser.add_argument(
        "--once",
        action="store_true",
        default=False,
        help="Run one poll cycle then exit",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Skip sending messages; log actions only",
    )
    args = parser.parse_args()
    exit_code = asyncio.run(_async_main(args))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
