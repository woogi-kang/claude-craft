"""Ultra-slow human-like verification script.

Validates the core workflow against live X while behaving exactly
like a bored person casually browsing Twitter on their Mac.

Single account only. No X API. Everything via Playwright browser.
Codex CLI (gpt-5.1-codex-mini) for tweet classification + reply/DM composition.

Pace: ~20 minutes per action (search, reply, DM)

Setup:
  1. Install codex CLI: npm i -g @openai/codex
  2. uv run playwright install chromium
  3. uv run python verify.py

Browser runs in HEADED mode. Each critical action asks for confirmation.
"""

from __future__ import annotations

import asyncio
import json
import os
import random
import sys
from pathlib import Path

from dotenv import load_dotenv
from playwright.async_api import BrowserContext, Page, async_playwright
from playwright_stealth import Stealth

load_dotenv(Path(__file__).parent / ".env")

# Keywords grouped by category for balanced random selection
KW_BROAD = [
    "渡韓美容",  # 도한미용
    "韓国肌管理",  # 한국 피부관리
    "韓国美容皮膚科",  # 한국 미용피부과
    "渡韓整形",  # 도한성형
]
KW_TREATMENT = [
    "ポテンツァ 韓国",  # 포텐자
    "ピコトーニング 韓国",  # 피코토닝
    "リジュラン 韓国",  # 리쥬란
    "シュリンク 韓国",  # 슈링크 리프팅
    "インモード 韓国",  # 인모드
]
KW_PAIN = [
    "韓国皮膚科 失敗",  # 한국 피부과 실패
    "韓国 シミ取り",  # 한국 기미제거
]


def pick_keywords(count: int = 5) -> list[str]:
    """Pick keywords evenly from each group, shuffled."""
    groups = [list(g) for g in (KW_BROAD, KW_TREATMENT, KW_PAIN)]
    for g in groups:
        random.shuffle(g)

    picked: list[str] = []
    # Round-robin across groups
    idx = 0
    while len(picked) < count:
        group = groups[idx % len(groups)]
        if group:
            picked.append(group.pop(0))
        idx += 1
        # All groups empty
        if all(len(g) == 0 for g in groups):
            break

    return picked


CLASSIFY_SYSTEM = """\
You classify Japanese tweets about Korean dermatology/beauty clinics.

Categories:
- needs_help: User had a bad experience, complaint, aftercare issue, treatment failure, \
upselling, language barrier. They need empathetic support.
- seeking_info: User is asking questions, comparing clinics, planning a visit, \
asking for recommendations, sharing prices. They need data-driven answers.
- irrelevant: Clinic marketing, bot, influencer promo, unrelated content, \
Korean account posing as Japanese, spam, news article share.

Rules:
1. Genuine personal questions/concerns = seeking_info or needs_help, NEVER irrelevant
2. Complaints, failures, worries = needs_help
3. "Which clinic?", "How much?", "Anyone been?" = seeking_info
4. Accounts promoting their own clinic = irrelevant
5. Simple retweets of news without personal comment = irrelevant

Reply ONLY valid JSON:
{"classification": "needs_help"|"seeking_info"|"irrelevant", "confidence": 0.0-1.0, \
"reason": "one line why"}
"""


# ─────────────────────────────────────────────
# Ultra-slow human behavior
# ─────────────────────────────────────────────


async def human_wait(label: str, min_s: float = 30, max_s: float = 90) -> None:
    """Wait a long random time, showing countdown."""
    delay = random.uniform(min_s, max_s)
    print(f"  ... {label} ({delay:.0f}s)")
    remaining = delay
    while remaining > 0:
        chunk = min(10, remaining)
        await asyncio.sleep(chunk)
        remaining -= chunk
        if remaining > 0:
            print(f"      {remaining:.0f}s remaining")


async def browse_timeline(page: Page) -> None:
    """Casually scroll the timeline like a real person."""
    print("  ... casually browsing timeline")
    await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30_000)
    await asyncio.sleep(random.uniform(3, 6))

    for _ in range(random.randint(2, 5)):
        scroll_dist = random.randint(200, 500)
        steps = random.randint(3, 6)
        for _ in range(steps):
            await page.mouse.wheel(0, scroll_dist / steps)
            await asyncio.sleep(random.uniform(0.05, 0.15))

        await asyncio.sleep(random.uniform(3, 12))

        viewport = page.viewport_size
        if viewport:
            x = random.randint(200, viewport["width"] - 200)
            y = random.randint(150, viewport["height"] - 150)
            await page.mouse.move(x, y, steps=random.randint(8, 20))
            await asyncio.sleep(random.uniform(1, 4))


async def visit_random_profile(page: Page) -> None:
    """Click on a random user profile and browse briefly."""
    print("  ... glancing at a profile")
    articles = await page.query_selector_all('article[data-testid="tweet"]')
    if not articles:
        await asyncio.sleep(random.uniform(5, 10))
        return

    article = random.choice(articles[:5])
    user_links = await article.query_selector_all('a[role="link"]')
    for link in user_links:
        href = await link.get_attribute("href")
        if href and href.startswith("/") and "/status/" not in href and not href.startswith("/i/"):
            await page.goto(f"https://x.com{href}", wait_until="domcontentloaded", timeout=20_000)
            await asyncio.sleep(random.uniform(4, 15))

            for _ in range(random.randint(1, 3)):
                await page.mouse.wheel(0, random.randint(200, 400))
                await asyncio.sleep(random.uniform(2, 5))

            await page.go_back()
            await asyncio.sleep(random.uniform(2, 5))
            return

    await asyncio.sleep(random.uniform(3, 8))


async def idle_behavior(page: Page) -> None:
    """Do random idle things a human would do between actions."""
    actions = [browse_timeline, visit_random_profile]
    choice = random.choice(actions)
    await choice(page)


async def ultra_slow_type(page: Page, selector: str, text: str) -> None:
    """Type extremely slowly with occasional pauses like thinking."""
    el = await page.wait_for_selector(selector, timeout=15_000)
    if not el:
        return

    await el.click()
    await asyncio.sleep(random.uniform(0.5, 1.5))

    for ch in text:
        await page.keyboard.type(ch, delay=random.randint(100, 300))

        if random.random() < 0.08:
            await asyncio.sleep(random.uniform(1.0, 4.0))

        if random.random() < 0.15:
            await asyncio.sleep(random.uniform(0.3, 1.0))


async def ultra_slow_type_content(page: Page, text: str) -> None:
    """Type content into focused element extremely slowly."""
    for ch in text:
        await page.keyboard.type(ch, delay=random.randint(120, 350))

        if random.random() < 0.1:
            await asyncio.sleep(random.uniform(1.5, 5.0))

        if random.random() < 0.12:
            await asyncio.sleep(random.uniform(0.5, 1.5))


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────


def ask(prompt: str) -> bool:
    ans = input(f"\n>>> {prompt} [y/n]: ").strip().lower()
    return ans in ("y", "yes", "")


def get_env(key: str, fallback: str = "") -> str:
    return os.getenv(key, fallback)


async def create_browser(pw, name: str) -> BrowserContext:
    user_data = Path(__file__).parent / "data" / "sessions" / name
    user_data.mkdir(parents=True, exist_ok=True)

    context = await pw.chromium.launch_persistent_context(
        user_data_dir=str(user_data),
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
        viewport={"width": 1280, "height": 800},
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        locale="ja-JP",
        timezone_id="Asia/Tokyo",
    )
    stealth = Stealth()
    page = context.pages[0] if context.pages else await context.new_page()
    await stealth.apply_stealth_async(page)
    return context


# ─────────────────────────────────────────────
# LLM (Codex CLI)
# ─────────────────────────────────────────────

CODEX_MODEL = "gpt-5.1-codex-mini"


def _run_codex(prompt: str) -> str:
    """Run codex exec with a prompt, return the last message text."""
    import shutil
    import subprocess
    import tempfile

    codex_path = shutil.which("codex")
    if not codex_path:
        print("    ERROR: codex CLI not found")
        return ""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        out_path = f.name

    try:
        result = subprocess.run(
            [
                codex_path,
                "exec",
                "-m",
                CODEX_MODEL,
                "--ephemeral",
                "-o",
                out_path,
                prompt,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0 and result.stderr:
            print(f"    Codex stderr: {result.stderr[:200]}")
        return Path(out_path).read_text().strip()
    except subprocess.TimeoutExpired:
        print("    Codex timed out after 120s")
        return ""
    except OSError as e:
        print(f"    Codex error: {e}")
        return ""
    finally:
        Path(out_path).unlink(missing_ok=True)


def _extract_json(raw: str) -> dict | None:
    """Extract JSON object from LLM output (may be wrapped in markdown)."""
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(raw[start:end])
        except json.JSONDecodeError:
            pass
    return None


def classify_tweet(tweet: dict) -> dict:
    """Classify a single tweet using Codex CLI."""
    content = tweet.get("content", "")
    username = tweet.get("username", "unknown")

    if not content or len(content.strip()) < 5:
        return {"classification": "irrelevant", "confidence": 1.0, "reason": "empty tweet"}

    prompt = f"{CLASSIFY_SYSTEM}\n\nTweet by @{username}:\n{content}"
    raw = _run_codex(prompt)

    if not raw:
        print(f"    Empty response for @{username}")
        return {"classification": "irrelevant", "confidence": 0.0, "reason": "empty response"}

    parsed = _extract_json(raw)
    if parsed and "classification" in parsed:
        return parsed

    print(f"    Could not parse JSON from: {raw[:150]}")
    return {"classification": "irrelevant", "confidence": 0.0, "reason": "parse error"}


def classify_batch(tweets: list[dict]) -> list[dict]:
    """Classify tweets via LLM and return only qualified ones."""
    qualified = []

    for tweet in tweets:
        result = classify_tweet(tweet)
        cls = result.get("classification", "irrelevant")
        conf = result.get("confidence", 0)
        reason = result.get("reason", "")

        tag = "PASS" if cls in ("needs_help", "seeking_info") else "SKIP"
        print(f"    [{tag}] @{tweet.get('username', '?')} | {cls} ({conf:.0%}) | {reason}")

        if cls in ("needs_help", "seeking_info") and conf >= 0.6:
            tweet["classification"] = cls
            tweet["confidence"] = conf
            tweet["reason"] = reason
            qualified.append(tweet)

    return qualified


# ─────────────────────────────────────────────
# LLM Composition (reply / DM)
# ─────────────────────────────────────────────

COMPOSE_REPLY_PROMPT = """\
You are @ask.nandemo, a neutral data-driven resource about Korean dermatology for Japanese users.

Write a short reply (max 140 chars Japanese) to this tweet.

Rules:
- Write in natural, warm Japanese (not robotic keigo)
- Be empathetic if the user had a bad experience
- Be informative if the user is asking a question
- Reference specific data when possible (e.g., clinic count, price range)
- Include a soft CTA like "詳しくはDMでもお答えできますよ" only if appropriate
- Do NOT be promotional or pushy
- Do NOT mention that you are an AI or bot
- Keep it concise - 1-2 sentences max

Context data:
- 韓国の皮膚科クリニック: 4,256院のデータあり
- 施術データ: 518種類の美容皮膚科施術
- 価格比較: 日韓の施術費用データあり

Tweet classification: {classification}
Tweet by @{username}:
{content}

Reply ONLY the reply text, nothing else. No quotes, no explanation.
"""

COMPOSE_DM_PROMPT = """\
You are @ask.nandemo, a neutral data-driven resource about Korean dermatology for Japanese users.

Write a short DM (max 200 chars Japanese) to this user.

Rules:
- Reference their specific tweet/concern
- Be personal and helpful
- Provide 1-2 specific data points (clinic count, price info, treatment options)
- Offer to answer more questions
- Write in natural, warm Japanese
- Do NOT be promotional, do NOT hard-sell
- Keep it to 2-3 sentences

Context data:
- 韓国の皮膚科クリニック: 4,256院のデータあり
- 施術データ: 518種類の美容皮膚科施術
- 価格帯: レーザー治療 3-15万ウォン、ボトックス 5-20万ウォン、ヒアルロン酸 15-50万ウォン

Tweet classification: {classification}
Their tweet by @{username}:
{content}

Reply ONLY the DM text, nothing else. No quotes, no explanation.
"""


def _llm_text(prompt: str) -> str:
    """Run LLM with a plain text prompt and return the output text."""
    return _run_codex(prompt)


def compose_reply(tweet: dict) -> str:
    """Use LLM to compose a reply for a tweet."""
    prompt = COMPOSE_REPLY_PROMPT.format(
        classification=tweet.get("classification", "seeking_info"),
        username=tweet.get("username", "unknown"),
        content=tweet.get("content", ""),
    )
    return _llm_text(prompt)


def compose_dm(tweet: dict) -> str:
    """Use LLM to compose a DM for a tweet author."""
    prompt = COMPOSE_DM_PROMPT.format(
        classification=tweet.get("classification", "seeking_info"),
        username=tweet.get("username", "unknown"),
        content=tweet.get("content", ""),
    )
    return _llm_text(prompt)


# ─────────────────────────────────────────────
# Step 1: Login
# ─────────────────────────────────────────────


async def step_login(pw, label: str = "nandemo") -> BrowserContext:
    print(f"\n{'=' * 50}")
    print("  Login")
    print(f"{'=' * 50}")

    ctx = await create_browser(pw, label)
    page = ctx.pages[0]

    await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30_000)
    await asyncio.sleep(random.uniform(3, 6))

    compose_btn = await page.query_selector('[data-testid="SideNav_NewTweet_Button"]')
    profile_link = await page.query_selector('[data-testid="AppTabBar_Profile_Link"]')

    if compose_btn or profile_link:
        print("  Already logged in! (session from previous run)")
        await human_wait("settling in", 5, 15)
        await browse_timeline(page)
        return ctx

    print("  Not logged in.")
    print("  ┌─────────────────────────────────────────┐")
    print("  │  Browser is open. Log in manually.      │")
    print("  │                                         │")
    print("  │  Google login, 2FA, whatever works.     │")
    print("  │  Session will be saved for next time.   │")
    print("  │                                         │")
    print("  │  When you see the home timeline,        │")
    print("  │  come back here and press Enter.        │")
    print("  └─────────────────────────────────────────┘")

    await page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded", timeout=30_000)

    input("\n>>> Press Enter after you've logged in... ")

    await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30_000)
    await asyncio.sleep(3)

    compose_btn = await page.query_selector('[data-testid="SideNav_NewTweet_Button"]')
    profile_link = await page.query_selector('[data-testid="AppTabBar_Profile_Link"]')

    if compose_btn or profile_link:
        print("  LOGIN SUCCESS - session saved!")
        await human_wait("browsing after login", 10, 30)
        await browse_timeline(page)
    else:
        print("  Could not verify login. Check browser.")
        if not ask("Continue anyway?"):
            await ctx.close()
            sys.exit(1)

    return ctx


# ─────────────────────────────────────────────
# Step 2: Search (ultra slow)
# ─────────────────────────────────────────────


async def step_search(ctx: BrowserContext, keyword: str) -> list[dict]:
    import urllib.parse

    print(f"\n{'=' * 50}")
    print(f"  Search: '{keyword}'")
    print(f"{'=' * 50}")

    page = ctx.pages[0]

    # Browse timeline casually before searching
    await browse_timeline(page)
    await human_wait("before searching", 15, 45)

    encoded = urllib.parse.quote(keyword)
    url = f"https://x.com/search?q={encoded}&src=typed_query&f=live"

    print("  Navigating to search...")
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
    await asyncio.sleep(random.uniform(4, 8))

    # Slow scroll, reading tweets
    for _ in range(random.randint(3, 6)):
        scroll_dist = random.randint(200, 500)
        steps = random.randint(3, 6)
        for _ in range(steps):
            await page.mouse.wheel(0, scroll_dist / steps)
            await asyncio.sleep(random.uniform(0.05, 0.15))

        await asyncio.sleep(random.uniform(3, 10))

        viewport = page.viewport_size
        if viewport:
            x = random.randint(200, viewport["width"] - 200)
            y = random.randint(150, viewport["height"] - 150)
            await page.mouse.move(x, y, steps=random.randint(5, 15))
            await asyncio.sleep(random.uniform(1, 3))

    # Extract tweets (more than before - up to 15 for LLM filtering)
    articles = await page.query_selector_all('article[data-testid="tweet"]')
    print(f"  Found {len(articles)} tweet elements")

    if len(articles) == 0:
        print("  WARNING: No tweets found!")
        title = await page.title()
        print(f"  Page title: {title}")
        print(f"  Current URL: {page.url}")

        testids = await page.evaluate("""
            () => Array.from(document.querySelectorAll('[data-testid]'))
                        .map(e => e.getAttribute('data-testid'))
                        .slice(0, 30)
        """)
        print(f"  Available testids: {testids}")
        return []

    seen_urls: set[str] = set()
    tweets = []
    for i, article in enumerate(articles[:15]):
        tweet: dict = {}

        # Full text (not truncated)
        text_el = await article.query_selector('[data-testid="tweetText"]')
        if text_el:
            tweet["content"] = (await text_el.inner_text()).strip()

        # Username
        user_links = await article.query_selector_all('a[role="link"]')
        for link in user_links:
            href = await link.get_attribute("href")
            if href and href.startswith("/") and "/status/" not in href:
                username = href.strip("/")
                if username and not username.startswith("i/"):
                    tweet["username"] = username
                    break

        # Tweet URL + ID
        time_el = await article.query_selector("time")
        if time_el:
            parent_a = await time_el.evaluate_handle("el => el.closest('a')")
            href = await parent_a.get_attribute("href") if parent_a else None
            if href:
                tweet["url"] = f"https://x.com{href}"
                parts = href.strip("/").split("/")
                if len(parts) >= 3 and parts[-2] == "status":
                    tweet["tweet_id"] = parts[-1]

        # Dedup by URL
        tweet_url = tweet.get("url", "")
        if tweet_url in seen_urls:
            continue
        if tweet_url:
            seen_urls.add(tweet_url)

        tweet["index"] = len(tweets) + 1
        tweets.append(tweet)

        # "Read" each tweet slowly
        await asyncio.sleep(random.uniform(1, 4))

    # Casually browse a bit after reading results
    if tweets and random.random() < 0.5:
        read_tweet = random.choice(tweets[:3])
        if read_tweet.get("url"):
            print(f"\n  ... reading tweet by @{read_tweet.get('username')}")
            await page.goto(read_tweet["url"], wait_until="domcontentloaded", timeout=20_000)
            await asyncio.sleep(random.uniform(5, 15))

            for _ in range(random.randint(1, 3)):
                await page.mouse.wheel(0, random.randint(200, 400))
                await asyncio.sleep(random.uniform(2, 5))

            await page.go_back()
            await asyncio.sleep(random.uniform(2, 5))

    return tweets


# ─────────────────────────────────────────────
# Step 2b: Smart Search (search + classify loop)
# ─────────────────────────────────────────────


async def smart_search(
    ctx: BrowserContext,
    target_count: int = 3,
    max_keywords: int = 5,
) -> list[dict]:
    """Search keywords from balanced random selection, classify each batch, stop when enough."""
    all_qualified: list[dict] = []
    seen_tweet_ids: set[str] = set()

    keywords = pick_keywords(max_keywords)
    print(f"\n  Target: {target_count} qualified tweets")
    print(f"  Keywords selected: {keywords}")

    for kw_index, keyword in enumerate(keywords):
        if len(all_qualified) >= target_count:
            break

        print(f"\n  --- Keyword {kw_index + 1}/{len(keywords)}: '{keyword}' ---")

        # Search
        raw_tweets = await step_search(ctx, keyword)

        if not raw_tweets:
            print("  No tweets for this keyword, trying next...")
            await human_wait("before next keyword", 20, 60)
            continue

        # Dedup against already-seen tweets
        new_tweets = []
        for t in raw_tweets:
            tid = t.get("tweet_id", "")
            if tid and tid not in seen_tweet_ids:
                seen_tweet_ids.add(tid)
                new_tweets.append(t)

        if not new_tweets:
            print("  All tweets already seen, trying next keyword...")
            await human_wait("before next keyword", 15, 40)
            continue

        print(f"\n  Classifying {len(new_tweets)} new tweets...")

        # Classify
        qualified = classify_batch(new_tweets)
        all_qualified.extend(qualified)

        remaining = target_count - len(all_qualified)
        print(f"\n  Qualified so far: {len(all_qualified)}/{target_count}")

        if remaining > 0 and kw_index < len(keywords) - 1:
            print(f"  Need {remaining} more. Moving to next keyword...")
            await human_wait("between keyword searches", 30, 90)

    return all_qualified


# ─────────────────────────────────────────────
# Step 3: Reply (ultra slow)
# ─────────────────────────────────────────────


async def step_reply(ctx: BrowserContext, tweet: dict, reply_text: str) -> bool:
    tweet_url = tweet.get("url")
    if not tweet_url:
        print("  No tweet URL")
        return False

    print(f"\n{'=' * 50}")
    print(f"  Reply to @{tweet.get('username', '?')}")
    print(f"  Tweet: {tweet.get('content', '?')[:60]}...")
    print(f"  Reply: {reply_text}")
    print(f"{'=' * 50}")

    if not ask("Send this reply?"):
        return False

    page = ctx.pages[0]

    await idle_behavior(page)
    await human_wait("before navigating to tweet", 20, 60)

    await page.goto(tweet_url, wait_until="domcontentloaded", timeout=30_000)
    await asyncio.sleep(random.uniform(4, 8))

    print("  ... reading the tweet carefully")
    await asyncio.sleep(random.uniform(5, 15))

    for _ in range(random.randint(1, 3)):
        await page.mouse.wheel(0, random.randint(150, 400))
        await asyncio.sleep(random.uniform(2, 5))

    await page.mouse.wheel(0, -random.randint(200, 500))
    await asyncio.sleep(random.uniform(2, 5))

    await human_wait("thinking about what to reply", 10, 30)

    reply_box = await page.query_selector('[data-testid="tweetTextarea_0"]')
    if not reply_box:
        reply_btn = await page.query_selector('[data-testid="reply"]')
        if reply_btn:
            await reply_btn.click()
            await asyncio.sleep(random.uniform(2, 4))
            reply_box = await page.query_selector('[data-testid="tweetTextarea_0"]')

    if not reply_box:
        print("  ERROR: Could not find reply textarea")
        testids = await page.evaluate("""
            () => Array.from(document.querySelectorAll('[data-testid]'))
                .map(e => e.getAttribute('data-testid'))
                .filter(t => /tweet|reply|Tweet|Reply/i.test(t))
        """)
        print(f"  Available testids: {testids}")
        return False

    await reply_box.click()
    await asyncio.sleep(random.uniform(0.5, 2.0))

    print("  ... composing reply")
    await ultra_slow_type_content(page, reply_text)

    await human_wait("re-reading reply before sending", 5, 15)

    send_btn = await page.query_selector('[data-testid="tweetButtonInline"]')
    if not send_btn:
        send_btn = await page.query_selector('[data-testid="tweetButton"]')

    if send_btn:
        await send_btn.click()
        await asyncio.sleep(random.uniform(3, 6))
        print("  REPLY SENT")

        await human_wait("after sending reply", 10, 30)
        return True

    print("  ERROR: Could not find send button")
    return False


# ─────────────────────────────────────────────
# Step 4: DM (ultra slow)
# ─────────────────────────────────────────────


async def step_dm(ctx: BrowserContext, username: str, dm_text: str) -> bool:
    print(f"\n{'=' * 50}")
    print(f"  DM @{username}")
    print(f"  Message: {dm_text}")
    print(f"{'=' * 50}")

    if not ask("Send this DM?"):
        return False

    page = ctx.pages[0]

    await idle_behavior(page)
    await human_wait("before opening DMs", 30, 90)

    print(f"  ... visiting @{username}'s profile first")
    await page.goto(f"https://x.com/{username}", wait_until="domcontentloaded", timeout=20_000)
    await asyncio.sleep(random.uniform(5, 15))

    for _ in range(random.randint(1, 3)):
        await page.mouse.wheel(0, random.randint(200, 400))
        await asyncio.sleep(random.uniform(3, 8))

    await human_wait("browsing their profile", 10, 30)

    print("  ... opening DM compose")
    await page.goto("https://x.com/messages/compose", wait_until="domcontentloaded", timeout=30_000)
    await asyncio.sleep(random.uniform(3, 6))

    search_input = await page.query_selector('[data-testid="searchPeople"]')
    if not search_input:
        search_input = await page.query_selector("input[placeholder]")

    if not search_input:
        print("  ERROR: Could not find user search input")
        return False

    await search_input.click()
    await asyncio.sleep(random.uniform(0.5, 1.5))

    print(f"  ... searching for @{username}")
    for ch in username:
        await page.keyboard.type(ch, delay=random.randint(100, 250))
        if random.random() < 0.1:
            await asyncio.sleep(random.uniform(0.5, 2.0))

    await asyncio.sleep(random.uniform(3, 6))

    user_result = await page.query_selector('[data-testid="TypeaheadUser"]')
    if user_result:
        await user_result.click()
        await asyncio.sleep(random.uniform(1, 3))
    else:
        print(f"  ERROR: @{username} not found in results")
        return False

    next_btn = await page.query_selector('[data-testid="nextButton"]')
    if next_btn:
        await next_btn.click()
        await asyncio.sleep(random.uniform(2, 5))

    dm_input = await page.query_selector('[data-testid="dmComposerTextInput"]')
    if not dm_input:
        print("  ERROR: Could not find DM input")
        return False

    await dm_input.click()
    await asyncio.sleep(random.uniform(1, 3))

    print("  ... composing DM")
    await human_wait("thinking about message", 5, 15)
    await ultra_slow_type_content(page, dm_text)

    await human_wait("re-reading DM", 5, 15)

    send_btn = await page.query_selector('[data-testid="dmComposerSendButton"]')
    if send_btn:
        await send_btn.click()
        await asyncio.sleep(random.uniform(3, 6))
        print("  DM SENT")

        await human_wait("lingering in DMs", 10, 30)
        return True

    print("  ERROR: Could not find DM send button")
    return False


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────


async def main() -> None:
    print("=" * 50)
    print("  X Outreach - Ultra Slow Verification")
    print("  Single account | Playwright | Codex classify")
    print("  Browser: HEADED (visible)")
    print("=" * 50)

    import shutil

    if not shutil.which("codex"):
        print("\n  ERROR: codex CLI not found. Install: npm i -g @openai/codex")
        sys.exit(1)
    print(f"  Codex CLI: OK (model: {CODEX_MODEL})")

    print("\nModes:")
    print("  1. Smart search only (search + LLM filter)")
    print("  2. Smart search -> Reply")
    print("  3. Smart search -> Reply -> DM (full)")

    choice = input("\nWhich? [1/2/3]: ").strip() or "1"

    target_str = input("Target tweet count (default: 3): ").strip() or "3"
    target_count = int(target_str) if target_str.isdigit() else 3

    async with async_playwright() as pw:
        ctx = await step_login(pw)

        # ── Smart Search ──
        qualified = await smart_search(ctx, target_count)

        if qualified:
            print(f"\n{'=' * 50}")
            print(f"  RESULTS: {len(qualified)} qualified tweets")
            print(f"{'=' * 50}")
            for i, t in enumerate(qualified, 1):
                cls = t.get("classification", "?")
                conf = t.get("confidence", 0)
                print(f"\n  [{i}] @{t.get('username', '?')} ({cls}, {conf:.0%})")
                print(f"      {t.get('content', '')[:80]}")
                if t.get("url"):
                    print(f"      {t['url']}")
        else:
            print("\n  No qualified tweets found across all keywords.")

        if choice == "1":
            if not ask("Done. Close browser?"):
                print("  Browser stays open. Ctrl+C to exit.")
                await asyncio.sleep(3600)
            await ctx.close()
            return

        # ── Reply ──
        if choice in ("2", "3") and qualified:
            print("\n  Which tweet to reply to?")
            for i, t in enumerate(qualified, 1):
                print(f"    {i}. @{t.get('username', '?')}: {t.get('content', '')[:50]}")

            pick = input("  Number (default: 1): ").strip() or "1"
            target = (
                qualified[int(pick) - 1]
                if pick.isdigit() and int(pick) <= len(qualified)
                else qualified[0]
            )

            # Gemini composes the reply
            print("\n  Gemini is composing a reply...")
            reply_text = compose_reply(target)

            if reply_text:
                print(f"\n  Draft reply: {reply_text}")
                edit = input("  Edit (Enter to keep, or type new): ").strip()
                if edit:
                    reply_text = edit
                await step_reply(ctx, target, reply_text)
            else:
                print("  Gemini failed to compose. Type manually:")
                reply_text = input(f"  Reply to @{target.get('username', '?')}: ").strip()
                if reply_text:
                    await step_reply(ctx, target, reply_text)

        if choice == "2":
            print("\n  Browser stays open 30s for verification...")
            await asyncio.sleep(30)
            await ctx.close()
            return

        # ── DM ──
        if choice == "3" and qualified:
            await human_wait("between reply and DM", 60, 180)

            dm_user = target.get("username", "")

            # Gemini composes the DM
            print("\n  Gemini is composing a DM...")
            dm_text = compose_dm(target)

            if dm_text:
                print(f"\n  Draft DM: {dm_text}")
                edit = input("  Edit (Enter to keep, or type new): ").strip()
                if edit:
                    dm_text = edit
                await step_dm(ctx, dm_user, dm_text)
            else:
                print("  Gemini failed to compose. Type manually:")
                dm_text = input(f"  DM to @{dm_user}: ").strip()
                if dm_text:
                    await step_dm(ctx, dm_user, dm_text)

        print("\n  Browser stays open 30s for verification...")
        await asyncio.sleep(30)
        await ctx.close()

    print("\n" + "=" * 50)
    print("  Verification complete!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
