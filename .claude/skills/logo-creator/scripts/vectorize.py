#!/usr/bin/env python3
"""
Convert raster logo to SVG using potrace (local, free).

Pipeline: PNG → grayscale → threshold → BMP → potrace → SVG

Usage:
    python3 vectorize.py input.png output.svg
    python3 vectorize.py input.png output.svg --threshold 128
    python3 vectorize.py input.png output.svg --invert  # For dark backgrounds
"""

import os
import shutil
import subprocess
import sys
import tempfile


def check_potrace() -> bool:
    """Check if potrace is installed."""
    return shutil.which("potrace") is not None


def vectorize(input_path: str, output_path: str, threshold: int = 128, invert: bool = False) -> bool:
    """
    Convert raster image to SVG via potrace.

    Args:
        input_path: Path to input image (PNG/JPG)
        output_path: Path to save SVG output
        threshold: Binarization threshold 0-255 (default: 128)
        invert: Invert colors before tracing (for dark backgrounds)
    """
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow required. Install: pip install pillow")
        return False

    if not check_potrace():
        print("Error: potrace not found.")
        print("Install: brew install potrace")
        return False

    print(f"Vectorizing: {input_path}")

    # Load and convert to grayscale
    img = Image.open(input_path).convert("L")

    if invert:
        from PIL import ImageOps
        img = ImageOps.invert(img)

    # Threshold to binary (1-bit BMP)
    img = img.point(lambda x: 0 if x < threshold else 255, "1")

    # Save as BMP (potrace input format)
    with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as tmp:
        tmp_bmp = tmp.name
        img.save(tmp_bmp)

    try:
        # Run potrace
        cmd = [
            "potrace",
            tmp_bmp,
            "-s",  # SVG output
            "-o", output_path,
            "--flat",  # No grouping
            "--turdsize", "2",  # Remove specks
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"potrace error: {result.stderr}")
            return False

        if os.path.exists(output_path) and os.path.getsize(output_path) > 50:
            size_kb = os.path.getsize(output_path) / 1024
            print(f"Saved: {output_path} ({size_kb:.1f} KB)")
            return True
        else:
            print("Error: SVG output is empty or missing")
            return False

    finally:
        os.unlink(tmp_bmp)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert logo to SVG via potrace")
    parser.add_argument("input", help="Input image path (PNG/JPG)")
    parser.add_argument("output", help="Output SVG path")
    parser.add_argument("--threshold", "-t", type=int, default=128, help="Binarization threshold (default: 128)")
    parser.add_argument("--invert", action="store_true", help="Invert colors before tracing")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    if not vectorize(args.input, args.output, args.threshold, args.invert):
        sys.exit(1)


if __name__ == "__main__":
    main()
