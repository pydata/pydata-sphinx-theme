"""Generate a simple placeholder image that displays its own size.

Used for example content in the docs, instead of relying on external services.

Usage::

    python docs/scripts/make_placeholder.py WIDTH HEIGHT OUTPUT \
        [--bg COLOR] [--fg COLOR]
"""

import argparse

from PIL import Image, ImageDraw, ImageFont


def make_placeholder(width, height, output, bg="#888888", fg="#ffffff"):
    """Write a ``width`` x ``height`` image with its size drawn in the center."""
    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    text = f"{width}x{height}"
    # default font is scalable in recent Pillow; scale it to ~1/5 of the width
    try:
        font = ImageFont.load_default(size=max(6, width // 5))
    except TypeError:  # old Pillow
        font = ImageFont.load_default()
    draw.text((width / 2, height / 2), text, fill=fg, font=font, anchor="mm")
    img.save(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("width", type=int)
    parser.add_argument("height", type=int)
    parser.add_argument("output")
    parser.add_argument("--bg", default="#888888")
    parser.add_argument("--fg", default="#ffffff")
    args = parser.parse_args()
    make_placeholder(args.width, args.height, args.output, args.bg, args.fg)
