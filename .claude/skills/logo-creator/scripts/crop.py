#!/usr/bin/env python3
"""
Crop whitespace from logo and center in 1:1 square.

Supports both RGB (white background) and RGBA (transparent background) images.

Usage:
    python3 crop.py input.png output.png
    python3 crop.py input.png output.png --padding 10
    python3 crop.py input.png output.png --threshold 230
"""

import sys
import os

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Error: Pillow and numpy required.")
    print("Install: pip install pillow numpy")
    sys.exit(1)


def crop_to_content(image_path: str, output_path: str, padding: int = 5, threshold: int = 240):
    """
    Crop whitespace/transparent area from image and center in 1:1 square.

    Args:
        image_path: Path to input image
        output_path: Path to save cropped image
        padding: Pixels of padding around content (default: 5)
        threshold: Pixel value threshold for "white" (default: 240)
    """
    img = Image.open(image_path)
    has_alpha = img.mode == "RGBA"

    if has_alpha:
        data = np.array(img)
        # Non-transparent pixels (alpha > 10)
        mask = data[:, :, 3] > 10
    else:
        img_rgb = img.convert("RGB")
        data = np.array(img_rgb)
        # Non-white pixels
        mask = (data[:, :, 0] < threshold) | (data[:, :, 1] < threshold) | (data[:, :, 2] < threshold)

    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)

    if not np.any(rows) or not np.any(cols):
        print(f"Warning: No content found in {image_path}")
        img.save(output_path)
        return output_path

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # Add padding
    h, w = data.shape[:2]
    top = max(0, rmin - padding)
    bottom = min(h, rmax + padding + 1)
    left = max(0, cmin - padding)
    right = min(w, cmax + padding + 1)

    # Crop to content
    cropped = img.crop((left, top, right, bottom))

    # Make square
    cw, ch = cropped.size
    size = max(cw, ch)

    # Create square canvas
    if has_alpha:
        square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    else:
        square = Image.new("RGB", (size, size), (255, 255, 255))

    # Center
    x = (size - cw) // 2
    y = (size - ch) // 2
    square.paste(cropped, (x, y))

    square.save(output_path, quality=95)

    content_w = cmax - cmin + 1
    content_h = rmax - rmin + 1
    print(f"Original:  {w}x{h}")
    print(f"Content:   {content_w}x{content_h}")
    print(f"Output:    {size}x{size}")
    print(f"Saved:     {output_path}")

    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Crop whitespace from logo")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--padding", type=int, default=5, help="Padding around content (default: 5)")
    parser.add_argument("--threshold", type=int, default=240, help="White threshold 0-255 (default: 240)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    crop_to_content(args.input, args.output, args.padding, args.threshold)


if __name__ == "__main__":
    main()
