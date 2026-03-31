import csv
import asyncio
import aiohttp
from pathlib import Path
from urllib.parse import urlparse

CSV_PATH = Path("intro_tip_links.csv")
OUT_DIR = Path("intro_tip_thumbnails")
OUT_DIR.mkdir(exist_ok=True)

CONCURRENT = 20  # 동시 다운로드 수
TIMEOUT = aiohttp.ClientTimeout(total=30)


async def download(session: aiohttp.ClientSession, sem: asyncio.Semaphore, row: dict):
    category = row["구분"]
    number = row["번호"]
    image_url = row["이미지URL"].strip()
    title = row["제품명"].strip()

    if not image_url:
        return ("skip", number, title, "이미지URL 없음")

    # 파일명: 구분_번호_제품명 (안전한 문자만)
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)[:50]
    if category == "쿠팡제품":
        filename = f"{number}_{safe_title}.webp"
    else:
        filename = f"{category}_{safe_title}.webp"

    filepath = OUT_DIR / filename
    if filepath.exists():
        return ("exists", number, title, str(filepath))

    async with sem:
        try:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    # Detect actual extension from content-type
                    ct = resp.headers.get("Content-Type", "")
                    if "jpeg" in ct or "jpg" in ct:
                        filepath = filepath.with_suffix(".jpg")
                    elif "png" in ct:
                        filepath = filepath.with_suffix(".png")
                    filepath.write_bytes(content)
                    return ("ok", number, title, str(filepath))
                else:
                    return ("error", number, title, f"HTTP {resp.status}")
        except Exception as e:
            return ("error", number, title, str(e)[:80])


async def main():
    rows = []
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    print(f"총 {len(rows)}개 행 로드")

    sem = asyncio.Semaphore(CONCURRENT)
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(timeout=TIMEOUT, connector=connector) as session:
        tasks = [download(session, sem, row) for row in rows]
        results = await asyncio.gather(*tasks)

    ok = sum(1 for r in results if r[0] == "ok")
    skip = sum(1 for r in results if r[0] == "skip")
    exists = sum(1 for r in results if r[0] == "exists")
    errors = [r for r in results if r[0] == "error"]

    print(f"\n=== 다운로드 완료 ===")
    print(f"성공: {ok}")
    print(f"스킵 (URL 없음): {skip}")
    print(f"이미 존재: {exists}")
    print(f"에러: {len(errors)}")

    if errors:
        print("\n에러 목록:")
        for e in errors[:20]:
            print(f"  #{e[1]} {e[2]}: {e[3]}")
        if len(errors) > 20:
            print(f"  ... 외 {len(errors) - 20}건")


if __name__ == "__main__":
    asyncio.run(main())
