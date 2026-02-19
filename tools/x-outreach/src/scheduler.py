"""APScheduler-based pipeline scheduler.

Runs ``PipelineRunner.run_once()`` at configured intervals during
active hours (JST).  Supports graceful shutdown on SIGINT/SIGTERM,
emergency halt detection, and SQLite-backed job persistence.
"""

from __future__ import annotations

import asyncio
import signal
from pathlib import Path
from typing import TYPE_CHECKING

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.interval import IntervalTrigger

from src.config import PROJECT_ROOT, Settings, load_settings
from src.pipeline.halt import HaltManager, get_volume_multiplier
from src.utils.logger import get_logger
from src.utils.time_utils import is_active_hours

if TYPE_CHECKING:
    from src.main import PipelineRunner

logger = get_logger("scheduler")

# Job ID used for the recurring pipeline run
_PIPELINE_JOB_ID = "pipeline_run"


class PipelineScheduler:
    """Schedule recurring pipeline runs using APScheduler.

    Parameters
    ----------
    runner:
        The pipeline runner that executes ``run_once()``.
    settings:
        Application settings including scheduling configuration.
    halt_manager:
        Emergency halt manager for checking halt state.
    db_path:
        Path to the SQLite database for job persistence.  Defaults to
        the project's ``data/scheduler_jobs.db``.
    """

    def __init__(
        self,
        runner: PipelineRunner,
        settings: Settings,
        halt_manager: HaltManager | None = None,
        db_path: Path | str | None = None,
    ) -> None:
        self._runner = runner
        self._settings = settings
        self._halt_manager = halt_manager or HaltManager()
        self._scheduler: AsyncIOScheduler | None = None
        self._running = False

        if db_path is None:
            db_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "scheduler_jobs.db"
            )
        self._db_path = Path(db_path)

        # Config hot-reload: track config.yaml modification time
        self._config_path = PROJECT_ROOT / "config.yaml"
        self._config_mtime: float = self._get_config_mtime()

    @property
    def is_running(self) -> bool:
        """Return ``True`` if the scheduler is actively running."""
        return self._running

    # ------------------------------------------------------------------
    # Config hot-reload
    # ------------------------------------------------------------------

    def _get_config_mtime(self) -> float:
        """Return the modification time of ``config.yaml``, or ``0.0``."""
        try:
            return self._config_path.stat().st_mtime
        except OSError:
            return 0.0

    def _check_config_reload(self) -> bool:
        """Reload settings if ``config.yaml`` has been modified.

        Returns
        -------
        bool
            ``True`` if the configuration was reloaded.
        """
        current_mtime = self._get_config_mtime()
        if current_mtime != self._config_mtime and current_mtime > 0:
            self._config_mtime = current_mtime
            try:
                self._settings = load_settings(self._config_path)
                logger.info(
                    "config_hot_reloaded",
                    config_path=str(self._config_path),
                )
                return True
            except Exception as exc:
                logger.error(
                    "config_reload_failed",
                    error=str(exc),
                )
        return False

    # ------------------------------------------------------------------
    # Core scheduling
    # ------------------------------------------------------------------

    def _create_scheduler(self) -> AsyncIOScheduler:
        """Build the APScheduler instance with SQLite job store."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        job_store_url = f"sqlite:///{self._db_path}"

        jobstores = {
            "default": SQLAlchemyJobStore(url=job_store_url),
        }

        scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            job_defaults={
                "coalesce": True,  # Merge missed runs into one
                "max_instances": 1,
                "misfire_grace_time": 3600,  # Allow 1 hour late execution
            },
        )
        return scheduler

    async def _run_pipeline_job(self) -> None:
        """Execute a single pipeline run with pre-flight checks.

        This is the function invoked by APScheduler on each interval.
        """
        # Check for config.yaml changes before each run
        self._check_config_reload()

        sched_cfg = self._settings.scheduling

        # Check emergency halt
        if self._halt_manager.is_halted():
            halt_info = self._halt_manager.get_halt_info()
            logger.warning(
                "pipeline_skipped_halted",
                reason=halt_info.get("reason", "unknown") if halt_info else "unknown",
            )
            return

        # Check active hours
        if not is_active_hours(sched_cfg.active_start_hour, sched_cfg.active_end_hour):
            logger.info(
                "pipeline_skipped_outside_hours",
                start=sched_cfg.active_start_hour,
                end=sched_cfg.active_end_hour,
            )
            return

        # Check volume multiplier (post-resume conservation)
        multiplier = get_volume_multiplier(self._halt_manager)
        dry_run = False
        if multiplier < 1.0:
            logger.info("conservation_mode_active", multiplier=multiplier)

        logger.info("pipeline_run_starting")

        try:
            result = await self._runner.run_once(dry_run=dry_run)
            if result.success:
                logger.info(
                    "pipeline_run_complete",
                    searched=result.search_count,
                    collected=result.collect.stored if result.collect else 0,
                    analyzed=result.analyze.total_processed if result.analyze else 0,
                )
            else:
                logger.error("pipeline_run_failed", error=result.error)

                # Check for restriction signals in error messages
                if result.error and self._halt_manager.is_restriction_error(
                    403, result.error
                ):
                    self._halt_manager.trigger_halt(
                        reason=f"Restriction detected: {result.error}",
                        source="pipeline",
                    )

        except Exception as exc:
            logger.error("pipeline_run_exception", error=str(exc))

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> AsyncIOScheduler:
        """Create and start the scheduler with the pipeline job.

        Returns
        -------
        AsyncIOScheduler
            The started scheduler instance.
        """
        if self._running:
            logger.warning("scheduler_already_running")
            return self._scheduler  # type: ignore[return-value]

        self._scheduler = self._create_scheduler()

        interval_hours = self._settings.scheduling.interval_hours
        trigger = IntervalTrigger(hours=interval_hours)

        self._scheduler.add_job(
            self._run_pipeline_job,
            trigger=trigger,
            id=_PIPELINE_JOB_ID,
            name="Pipeline Run",
            replace_existing=True,
        )

        self._scheduler.start()
        self._running = True

        logger.info(
            "scheduler_started",
            interval_hours=interval_hours,
            active_start=self._settings.scheduling.active_start_hour,
            active_end=self._settings.scheduling.active_end_hour,
        )

        return self._scheduler

    def stop(self) -> None:
        """Shut down the scheduler gracefully."""
        if self._scheduler is not None and self._running:
            self._scheduler.shutdown(wait=True)
            self._running = False
            logger.info("scheduler_stopped")

    async def run_forever(self) -> None:
        """Start the scheduler and block until a shutdown signal is received.

        Installs SIGINT and SIGTERM handlers for graceful shutdown.
        """
        loop = asyncio.get_running_loop()
        stop_event = asyncio.Event()

        def _signal_handler() -> None:
            logger.info("shutdown_signal_received")
            stop_event.set()

        # Install signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, _signal_handler)

        self.start()

        # Run the first job immediately if we missed a scheduled run
        logger.info("running_initial_job")
        await self._run_pipeline_job()

        # Block until shutdown signal
        await stop_event.wait()

        self.stop()
        logger.info("scheduler_exited")
