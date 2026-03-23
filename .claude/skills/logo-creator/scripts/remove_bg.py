#!/usr/bin/env python3
"""
Remove background from logo using rembg (local, free, no API key).

Falls back to simple white-removal if rembg is not installed.

Usage:
    python3 remove_bg.py input.png output.png
    python3 remove_bg.py input.png output.png --method rembg     # AI-based (default)
    python3 remove_bg.py input.png output.png --method threshold  # Simple white removal
"""

import sys
import os


def remove_bg_rembg(input_path: str, output_path: str) -> bool:
    """Remove background using rembg (AI-based, local)."""
    try:
        from rembg import remove
        from PIL import Image
    except ImportError:
        return False

    print(f"Removing background (rembg)...")
    img = Image.open(input_path)
    result = remove(img)
    result.save(output_path)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"Saved: {output_path} ({size_kb:.1f} KB)")
    return True


def remove_bg_threshold(input_path: str, output_path: str, threshold: int = 240) -> bool:
    """Remove white background using simple thresholding."""
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        print("Error: Pillow and numpy required. Install: pip install pillow numpy")
        return False

    print(f"Removing background (threshold={threshold})...")
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)

    # White-ish pixels become transparent
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    white_mask = (r > threshold) & (g > threshold) & (b > threshold)
    data[white_mask, 3] = 0

    result = Image.fromarray(data)
    result.save(output_path)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"Saved: {output_path} ({size_kb:.1f} KB)")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Remove background from logo")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path (transparent PNG)")
    parser.add_argument(
        "--method",
        choices=["rembg", "threshold"],
        default="rembg",
        help="Removal method (default: rembg)",
    )
    parser.add_argument("--threshold", type=int, default=240, help="White threshold for threshold method")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    if args.method == "rembg":
        if not remove_bg_rembg(args.input, args.output):
            print("rembg not installed. Falling back to threshold method.")
            print("For better results: pip install rembg")
            if not remove_bg_threshold(args.input, args.output, args.threshold):
                sys.exit(1)
    else:
        if not remove_bg_threshold(args.input, args.output, args.threshold):
            sys.exit(1)


if __name__ == "__main__":
    main()
