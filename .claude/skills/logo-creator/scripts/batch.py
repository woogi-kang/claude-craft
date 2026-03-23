#!/usr/bin/env python3
"""
Logo Batch Generator - 20+ 로고 변형을 한번에 생성하고 HTML 프리뷰를 자동 생성.

Usage:
    python3 batch.py --brand "TechFlow" --prompt "innovative tech startup" --count 20
    python3 batch.py --brand "CafeBloom" --industry food --count 10 --pro
    python3 batch.py --brand "TechFlow" --prompt "feedback-based refinement" --prefix "logo-05-v" --count 5

Models:
    - Default: gemini-2.5-flash-image (fast, high-volume)
    - --pro:   gemini-3-pro-image-preview (professional quality)
"""

import argparse
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# Load environment variables
def load_env():
    env_paths = [
        Path(__file__).parent.parent / ".env",
        Path(__file__).parents[2] / "design" / ".env",
        Path.home() / ".claude" / "skills" / ".env",
        Path.home() / ".claude" / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key not in os.environ:
                            os.environ[key] = value.strip("\"'")

load_env()

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)


# ============ CONFIGURATION ============
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_FLASH = "gemini-2.5-flash-image"
GEMINI_PRO = "gemini-3-pro-image-preview"

ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4"]

LOGO_PROMPT_TEMPLATE = """Generate a professional logo image: {prompt}

Style requirements:
- Clean vector-style illustration suitable for a logo
- Simple, scalable design that works at any size
- Clear silhouette and recognizable shape
- Professional quality suitable for business use
- Centered composition on plain white background
- No text unless specifically requested
- High contrast and clear edges
- Square format, perfectly centered
- Output as a clean, high-quality logo image
"""

# 20 distinct styles for batch generation
BATCH_STYLES = [
    ("minimalist", "minimalist, simple geometric shapes, clean lines, lots of white space, single color"),
    ("modern", "modern, sleek gradient, tech-forward, innovative feel, smooth curves"),
    ("geometric", "geometric, abstract patterns, mathematical precision, symmetrical"),
    ("gradient", "gradient, vibrant color transitions, modern digital feel, smooth flow"),
    ("abstract", "abstract mark, conceptual, symbolic, non-literal representation"),
    ("lettermark", "lettermark, stylized initial letter, typographic, monogram style"),
    ("negative-space", "negative space, clever use of white space, hidden meaning, dual imagery"),
    ("lineart", "line art, single stroke, continuous line, elegant simplicity"),
    ("3d", "3D, dimensional, depth, soft shadows, isometric perspective"),
    ("vintage", "vintage, retro, badge style, heritage feel, warm earth tones"),
    ("emblem", "emblem, badge, crest style, enclosed design, traditional"),
    ("mascot", "mascot, character, friendly face, memorable figure, cartoon"),
    ("hand-drawn", "hand-drawn, sketch-like, artistic strokes, organic lines"),
    ("luxury", "luxury, elegant, gold accents, refined, premium feel, serif"),
    ("flat", "flat design, solid colors, no gradients, clean sharp edges"),
    ("pixel-art", "pixel art, 8-bit retro style, blocky pixels, sharp edges, no anti-aliasing"),
    ("monoline", "monoline, single weight stroke, continuous path, uniform thickness"),
    ("wordmark", "wordmark, custom typography, brand name as logo, distinctive lettering"),
    ("circular", "circular composition, round badge, contained within circle"),
    ("organic", "organic, natural flowing lines, leaf or nature elements, earthy"),
]

INDUSTRY_CONTEXT = {
    "tech": "technology company, digital, innovative, circuit-like elements",
    "healthcare": "healthcare, medical, caring, trust, cross or heart symbol",
    "finance": "financial services, stable, trustworthy, growth, upward elements",
    "food": "food and beverage, appetizing, warm colors, welcoming",
    "fashion": "fashion brand, elegant, stylish, refined, artistic",
    "fitness": "fitness and sports, dynamic, energetic, powerful, movement",
    "eco": "eco-friendly, sustainable, natural, green, leaf or earth elements",
    "education": "education, knowledge, growth, learning, book or cap symbol",
    "real-estate": "real estate, property, home, roof or building silhouette",
    "creative": "creative agency, artistic, unique, expressive, colorful",
    "gaming": "gaming, playful, dynamic, bold colors, action",
    "beauty": "beauty, cosmetics, elegant, soft colors, delicate",
    "legal": "legal, law firm, authoritative, balanced, scales or pillar",
    "consulting": "consulting, professional, strategic, abstract growth",
    "music": "music, entertainment, rhythm, sound waves, dynamic",
}


def generate_single(client, prompt: str, model: str, aspect_ratio: str, output_path: str) -> bool:
    """Generate a single logo image."""
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
                image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
            ),
        )

        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                if part.inline_data.mime_type.startswith("image/"):
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    return True

        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False


def build_prompt(base_prompt: str, style_desc: str, brand: str = None, industry: str = None) -> str:
    """Build enhanced prompt from components."""
    parts = []
    if brand:
        parts.append(f"Logo for '{brand}':")
    parts.append(base_prompt)
    parts.append(style_desc)
    if industry and industry in INDUSTRY_CONTEXT:
        parts.append(INDUSTRY_CONTEXT[industry])

    return LOGO_PROMPT_TEMPLATE.format(prompt=", ".join(parts))


def copy_preview_template(output_dir: str, count: int, prefix: str = "logo-"):
    """Generate preview.html with correct number of logos."""
    template_path = Path(__file__).parent.parent / "templates" / "preview.html"
    if not template_path.exists():
        print(f"Warning: preview.html template not found at {template_path}")
        return

    with open(template_path, "r") as f:
        html = f.read()

    # Generate logo card entries
    cards = []
    for i in range(1, count + 1):
        filename = f"{prefix}{i:02d}.png"
        cards.append(
            f'    <div class="logo-card" data-src="{filename}" onclick="showModal(this)">\n'
            f'      <img src="{filename}" onerror="this.parentElement.style.display=\'none\'">\n'
            f"      <p>#{i:02d}</p>\n"
            f"    </div>"
        )

    # Replace placeholder cards
    card_html = "\n".join(cards)
    html = html.replace("<!-- LOGO_CARDS_PLACEHOLDER -->", card_html)

    # Remove example cards (between placeholder and closing grid div)
    import re
    html = re.sub(
        r'<!-- Example cards.*?(?=\s*</div>\s*\n\s*<div class="favorites-bar">)',
        "",
        html,
        flags=re.DOTALL,
    )

    output_path = os.path.join(output_dir, "preview.html")
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Preview: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Logo Batch Generator")
    parser.add_argument("--brand", "-b", type=str, help="Brand name")
    parser.add_argument("--prompt", "-p", type=str, default="professional logo", help="Logo description")
    parser.add_argument("--industry", "-i", choices=list(INDUSTRY_CONTEXT.keys()), help="Industry type")
    parser.add_argument("--count", "-n", type=int, default=20, help="Number of variants (default: 20)")
    parser.add_argument("--output-dir", "-d", type=str, help="Output directory")
    parser.add_argument("--prefix", type=str, default="logo-", help="Filename prefix (default: logo-)")
    parser.add_argument("--pro", action="store_true", help="Use Gemini Pro for higher quality")
    parser.add_argument("--aspect-ratio", "-r", choices=ASPECT_RATIOS, default="1:1", help="Aspect ratio")
    parser.add_argument("--styles", type=str, help="Comma-separated style names to use (e.g. minimalist,modern,3d)")
    parser.add_argument("--delay", type=float, default=3.0, help="Delay between requests in seconds (default: 3)")
    parser.add_argument("--no-preview", action="store_true", help="Skip preview.html generation")

    args = parser.parse_args()

    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set")
        print("Set with: export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
        brand_slug = (args.brand or "logo").lower().replace(" ", "-")
        output_dir = f".skill-output/logo-creator/{date_str}-{brand_slug}"

    os.makedirs(output_dir, exist_ok=True)

    # Select styles
    if args.styles:
        style_names = [s.strip() for s in args.styles.split(",")]
        styles = [(name, desc) for name, desc in BATCH_STYLES if name in style_names]
        if not styles:
            print(f"Error: No matching styles. Available: {', '.join(s[0] for s in BATCH_STYLES)}")
            sys.exit(1)
    else:
        styles = BATCH_STYLES

    # Limit count
    count = min(args.count, len(styles))
    if args.count > len(styles):
        print(f"Note: Using {len(styles)} styles (max available). Request was {args.count}.")
        count = len(styles)

    model = GEMINI_PRO if args.pro else GEMINI_FLASH
    model_label = "Gemini Pro" if args.pro else "Gemini Flash"

    print(f"\n{'=' * 60}")
    print(f"  LOGO BATCH GENERATION")
    print(f"  Brand: {args.brand or 'N/A'}")
    print(f"  Model: {model_label}")
    print(f"  Count: {count}")
    print(f"  Ratio: {args.aspect_ratio}")
    print(f"  Output: {output_dir}")
    print(f"{'=' * 60}\n")

    client = genai.Client(api_key=GEMINI_API_KEY)
    success = 0
    failed = 0

    for i in range(count):
        style_name, style_desc = styles[i]
        filename = f"{args.prefix}{i + 1:02d}.png"
        output_path = os.path.join(output_dir, filename)

        prompt = build_prompt(args.prompt, style_desc, args.brand, args.industry)

        print(f"[{i + 1}/{count}] {style_name}...", end=" ", flush=True)

        if generate_single(client, prompt, model, args.aspect_ratio, output_path):
            print(f"OK -> {filename}")
            success += 1
        else:
            print("FAILED")
            failed += 1

        if i < count - 1:
            time.sleep(args.delay)

    print(f"\n{'=' * 60}")
    print(f"  COMPLETE: {success}/{count} generated ({failed} failed)")
    print(f"  Output: {output_dir}")
    print(f"{'=' * 60}\n")

    # Generate preview HTML
    if not args.no_preview and success > 0:
        copy_preview_template(output_dir, count, args.prefix)
        print(f"\nOpen preview: open {output_dir}/preview.html")


if __name__ == "__main__":
    main()
