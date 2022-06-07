import sys
import numpy as np
from PIL import Image
import argparse
import os

colours = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "yellow": (255, 255, 0),
}


def center_crop(image, size):
    w, h = image.size

    left = (w - size) / 2
    top = (h - size) / 2
    right = (w + size) / 2
    bottom = (h + size) / 2

    resized = image.resize((w, h))
    cropped = resized.crop((left, top, right, bottom))

    return cropped


def nearest_colour(rgb):
    return min(
        list(colours.values()),
        key=lambda colour: sum((s - q) ** 2 for s, q in zip(colour, rgb)),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pixelate")
    parser.add_argument("--img", type=str)
    parser.add_argument("--size", type=int, default=1024, choices=[256, 512, 1024, 2048])
    parser.add_argument("--factor", type=int, default=1, choices=[1, 2, 5])
    parser.add_argument("--outdir", type=str, required=True)
    args = parser.parse_args()

    IMAGE = args.img
    SIZE = args.size
    FACTOR = args.factor
    OUT_DIR = args.outdir

    os.makedirs(OUT_DIR, exist_ok=True)
    filename = os.path.basename(IMAGE)

    image = Image.open(IMAGE)
    image = center_crop(image, SIZE)
    # image = image.resize((SIZE, SIZE))
    image = image.convert("RGB")
    factor = FACTOR

    small = image.resize((40 * 2 * factor, 25 * 3 * factor), resample=Image.BILINEAR)
    pixels = np.asarray(small).copy()
    (w, h, _) = pixels.shape

    for x in range(w):
        for y in range(h):
            pixels[x][y] = nearest_colour(pixels[x][y])

    mode7 = Image.fromarray(pixels)
    result = mode7.resize(image.size, Image.NEAREST)

    result.save(os.path.join(OUT_DIR, filename))
