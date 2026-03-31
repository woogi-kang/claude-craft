"""Video presence analyzer: detects embedded videos and social media profiles."""

import re
from urllib.parse import urlparse

VIDEO_EMBED_PATTERNS: dict[str, list[str]] = {
    "youtube": [
        r'<iframe[^>]+src=["\'][^"\']*youtube\.com/embed/([^"\'?]+)',
        r'<iframe[^>]+src=["\'][^"\']*youtu\.be/([^"\'?]+)',
    ],
    "naver_tv": [
        r'<iframe[^>]+src=["\'][^"\']*tv\.naver\.com/([^"\'?]+)',
    ],
    "vimeo": [
        r'<iframe[^>]+src=["\'][^"\']*(?:player\.)?vimeo\.com/(?:video/)?([^"\'?]+)',
    ],
    "self_hosted": [
        r'<video[^>]+src=["\']([^"\']+)',
        r'<video[^>]*>.*?<source[^>]+src=["\']([^"\']+)',
    ],
}

VIDEO_LINK_PATTERNS: dict[str, list[str]] = {
    "youtube": [r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+'],
    "naver_tv": [r'https?://tv\.naver\.com/v/\d+'],
    "vimeo": [r'https?://vimeo\.com/\d+'],
}

SOCIAL_PATTERNS: dict[str, list[str]] = {
    "youtube": [r'youtube\.com/(channel|c|user)/[\w.-]+', r'youtube\.com/@[\w.-]+'],
    "instagram": [r'instagram\.com/[\w.]+/?$'],
    "tiktok": [r'tiktok\.com/@[\w.]+'],
    "facebook": [r'facebook\.com/[\w.]+/?$'],
    "naver_blog": [r'blog\.naver\.com/[\w]+'],
    "naver_tv": [r'tv\.naver\.com/[\w]+'],
    "kakao_story": [r'story\.kakao\.com/[\w]+'],
    "xiaohongshu": [r'xiaohongshu\.com/', r'xhslink\.com/'],
    "twitter": [r'(?:twitter|x)\.com/[\w]+/?$'],
}

SOCIAL_LABELS: dict[str, str] = {
    "youtube": "YouTube",
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "facebook": "Facebook",
    "naver_blog": "네이버 블로그",
    "naver_tv": "네이버 TV",
    "kakao_story": "카카오스토리",
    "xiaohongshu": "小红书",
    "twitter": "Twitter/X",
}

# URLs to exclude from social profile detection (common false positives)
_SOCIAL_EXCLUDE = {
    "facebook": {r'facebook\.com/sharer', r'facebook\.com/tr', r'facebook\.com/plugins'},
    "twitter": {r'twitter\.com/intent', r'twitter\.com/share', r'x\.com/intent'},
}


def _extract_urls(html: str) -> list[str]:
    """Extract all href and src URLs from HTML."""
    return re.findall(r'(?:href|src)=["\']([^"\']+)', html, re.IGNORECASE)


def _extract_embedded_videos(html: str) -> dict[str, dict]:
    """Find embedded videos in HTML."""
    results: dict[str, dict] = {}
    for platform, patterns in VIDEO_EMBED_PATTERNS.items():
        urls: list[str] = []
        for pattern in patterns:
            for match in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
                url = match.group(0) if platform == "self_hosted" else match.group(0)
                # Extract the src URL from the full match
                src_match = re.search(r'src=["\']([^"\']+)', match.group(0))
                if src_match:
                    url = src_match.group(1)
                elif platform == "self_hosted":
                    url = match.group(1)
                if url and url not in urls:
                    urls.append(url)
        results[platform] = {"count": len(urls), "urls": urls}
    return results


def _extract_video_links(html: str) -> dict[str, list[str]]:
    """Find video links (non-embed) in HTML."""
    results: dict[str, list[str]] = {}
    for platform, patterns in VIDEO_LINK_PATTERNS.items():
        urls: list[str] = []
        for pattern in patterns:
            for match in re.finditer(pattern, html, re.IGNORECASE):
                url = match.group(0)
                if url not in urls:
                    urls.append(url)
        results[platform] = urls
    return results


def _detect_social_profiles(html: str) -> dict[str, dict]:
    """Detect social media profile links."""
    all_urls = _extract_urls(html)
    profiles: dict[str, dict] = {}

    for platform, patterns in SOCIAL_PATTERNS.items():
        found_url = None
        exclude_patterns = _SOCIAL_EXCLUDE.get(platform, set())

        for url in all_urls:
            # Skip excluded patterns (share buttons, tracking pixels)
            if any(re.search(ep, url, re.IGNORECASE) for ep in exclude_patterns):
                continue
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    found_url = url
                    break
            if found_url:
                break

        profiles[platform] = {
            "found": found_url is not None,
            "url": found_url,
            "label": SOCIAL_LABELS[platform],
        }

    return profiles


def _check_video_metadata(html: str) -> dict[str, bool]:
    """Check for video-related metadata."""
    has_og_video = bool(re.search(
        r'<meta[^>]+property=["\']og:video["\']', html, re.IGNORECASE
    ))
    has_video_schema = bool(re.search(
        r'"@type"\s*:\s*"VideoObject"', html, re.IGNORECASE
    ))
    return {"has_og_video": has_og_video, "has_video_schema": has_video_schema}


def _calculate_video_score(
    embedded: dict[str, dict],
    total_videos: int,
    has_youtube_channel: bool,
    has_video_schema: bool,
    has_og_video: bool,
) -> int:
    """Calculate video content score (0-100)."""
    score = 0

    # Embedded videos exist: 30 points
    if total_videos > 0:
        score += 30

    # 3+ videos: +15 points
    if total_videos >= 3:
        score += 15

    # YouTube channel: 20 points
    if has_youtube_channel:
        score += 20

    # Self-hosted video: 15 points
    if embedded.get("self_hosted", {}).get("count", 0) > 0:
        score += 15

    # VideoObject Schema: 10 points
    if has_video_schema:
        score += 10

    # og:video: 10 points
    if has_og_video:
        score += 10

    return min(score, 100)


def _calculate_social_score(profiles: dict[str, dict]) -> int:
    """Calculate social media presence score (0-100)."""
    found_count = sum(1 for p in profiles.values() if p["found"])
    # 15 points per profile, max 100
    score = min(found_count * 15, 100)

    # Bonus for TikTok or Xiaohongshu
    if profiles.get("tiktok", {}).get("found"):
        score = min(score + 10, 100)
    if profiles.get("xiaohongshu", {}).get("found"):
        score = min(score + 10, 100)

    return score


def _build_missing_platforms(profiles: dict[str, dict]) -> list[dict]:
    """Identify missing high-value platforms."""
    missing: list[dict] = []

    platform_priorities = {
        "tiktok": {"reason": "20-30대 환자 유입 기회", "priority": "high"},
        "xiaohongshu": {"reason": "중국 환자 대상 최고 효율 채널", "priority": "high"},
        "youtube": {"reason": "시술 과정 영상으로 신뢰도 향상", "priority": "high"},
        "instagram": {"reason": "비포/애프터 사진으로 시각적 어필", "priority": "high"},
        "naver_blog": {"reason": "국내 검색 유입의 핵심 채널", "priority": "medium"},
        "naver_tv": {"reason": "국내 환자 유입", "priority": "medium"},
        "facebook": {"reason": "동남아/글로벌 환자 소통 채널", "priority": "medium"},
        "twitter": {"reason": "글로벌 브랜드 인지도", "priority": "low"},
        "kakao_story": {"reason": "국내 40-50대 환자 소통", "priority": "low"},
    }

    for platform, info in platform_priorities.items():
        if not profiles.get(platform, {}).get("found"):
            missing.append({
                "platform": SOCIAL_LABELS.get(platform, platform),
                "reason": info["reason"],
                "priority": info["priority"],
            })

    return missing


def _build_recommendations(
    embedded: dict[str, dict],
    total_videos: int,
    profiles: dict[str, dict],
    has_video_schema: bool,
    has_og_video: bool,
    missing_platforms: list[dict],
) -> list[dict]:
    """Build actionable recommendations."""
    recs: list[dict] = []

    # High priority missing platforms
    for mp in missing_platforms:
        if mp["priority"] == "high":
            recs.append({
                "priority": "high",
                "message": f'{mp["platform"]} 미진출: {mp["reason"]}',
            })

    # Video content recommendations
    if total_videos == 0:
        recs.append({
            "priority": "high",
            "message": "영상 콘텐츠가 없습니다. 시술 과정, 의사 인터뷰 등 영상을 추가하면 환자 신뢰도가 크게 향상됩니다.",
        })
    elif total_videos < 3:
        recs.append({
            "priority": "medium",
            "message": f"영상 콘텐츠가 {total_videos}개로 부족합니다. 시술 과정 영상을 추가하세요.",
        })

    # Medium priority missing platforms
    for mp in missing_platforms:
        if mp["priority"] == "medium":
            recs.append({
                "priority": "medium",
                "message": f'{mp["platform"]} 미진출: {mp["reason"]}',
            })

    # Metadata recommendations
    if not has_video_schema and total_videos > 0:
        recs.append({
            "priority": "low",
            "message": "VideoObject Schema를 추가하면 검색에서 비디오 미리보기가 표시됩니다.",
        })
    if not has_og_video and total_videos > 0:
        recs.append({
            "priority": "low",
            "message": "og:video 메타 태그를 추가하면 소셜 미디어 공유 시 영상이 자동 재생됩니다.",
        })

    return recs


def analyze_video_presence(pages: list[dict]) -> dict:
    """Analyze video content and social media presence from crawled pages.

    Args:
        pages: list of dicts with "url" and "html" keys.

    Returns:
        Dict with embedded_videos, social_profiles, scores, and recommendations.
    """
    if not pages:
        empty_embedded = {p: {"count": 0, "urls": []} for p in VIDEO_EMBED_PATTERNS}
        empty_profiles = {
            p: {"found": False, "url": None, "label": SOCIAL_LABELS[p]}
            for p in SOCIAL_PATTERNS
        }
        return {
            "embedded_videos": empty_embedded,
            "total_videos": 0,
            "social_profiles": empty_profiles,
            "social_count": 0,
            "has_video_schema": False,
            "has_og_video": False,
            "video_score": 0,
            "social_score": 0,
            "overall_score": 0,
            "missing_platforms": [],
            "recommendations": [],
        }

    # Aggregate across all pages
    all_embedded: dict[str, dict] = {p: {"count": 0, "urls": []} for p in VIDEO_EMBED_PATTERNS}
    all_profiles: dict[str, dict] = {}
    has_video_schema = False
    has_og_video = False

    for page in pages:
        html = page.get("html", "")

        # Embedded videos
        page_embedded = _extract_embedded_videos(html)
        for platform, data in page_embedded.items():
            for url in data["urls"]:
                if url not in all_embedded[platform]["urls"]:
                    all_embedded[platform]["urls"].append(url)
            all_embedded[platform]["count"] = len(all_embedded[platform]["urls"])

        # Also check video links
        video_links = _extract_video_links(html)
        for platform, urls in video_links.items():
            if platform in all_embedded:
                for url in urls:
                    if url not in all_embedded[platform]["urls"]:
                        all_embedded[platform]["urls"].append(url)
                all_embedded[platform]["count"] = len(all_embedded[platform]["urls"])

        # Social profiles (first found wins)
        page_profiles = _detect_social_profiles(html)
        for platform, info in page_profiles.items():
            if platform not in all_profiles or (not all_profiles[platform]["found"] and info["found"]):
                all_profiles[platform] = info

        # Metadata
        meta = _check_video_metadata(html)
        if meta["has_video_schema"]:
            has_video_schema = True
        if meta["has_og_video"]:
            has_og_video = True

    # Fill in any missing social platforms
    for platform in SOCIAL_PATTERNS:
        if platform not in all_profiles:
            all_profiles[platform] = {
                "found": False,
                "url": None,
                "label": SOCIAL_LABELS[platform],
            }

    total_videos = sum(e["count"] for e in all_embedded.values())
    social_count = sum(1 for p in all_profiles.values() if p["found"])

    has_youtube_channel = all_profiles.get("youtube", {}).get("found", False)

    video_score = _calculate_video_score(
        all_embedded, total_videos, has_youtube_channel, has_video_schema, has_og_video
    )
    social_score = _calculate_social_score(all_profiles)
    overall_score = round(video_score * 0.5 + social_score * 0.5)

    missing_platforms = _build_missing_platforms(all_profiles)

    recommendations = _build_recommendations(
        all_embedded, total_videos, all_profiles,
        has_video_schema, has_og_video, missing_platforms,
    )

    return {
        "embedded_videos": all_embedded,
        "total_videos": total_videos,
        "social_profiles": all_profiles,
        "social_count": social_count,
        "has_video_schema": has_video_schema,
        "has_og_video": has_og_video,
        "video_score": video_score,
        "social_score": social_score,
        "overall_score": overall_score,
        "missing_platforms": missing_platforms,
        "recommendations": recommendations,
    }
