import argparse
import glob
from pathlib import Path
import random
from tkinter import Y
from PIL import Image, ImageOps

def get_samples(sample_names):
    samples = []
    for sample_name in sample_names:
        sample = Image.open(sample_name)
        samples.append(sample)
    return samples

def is_darker(pixel1, pixel2):
    return sum(pixel1) < sum(pixel2)

def pixel_within_bounds(position, image):
    return position[0] < image.width and position[1] < image.height

def place_sample(image, sample, position):
    for x in range(sample.width):
        for y in range(sample.height):
            image_position = (position[0] + x, position[1] + y)
            if pixel_within_bounds(image_position, image):
                sample_pixel = sample.getpixel((x, y))
                image_pixel = image.getpixel(image_position)
                if is_darker(sample_pixel, image_pixel):
                    image.putpixel(image_position, sample_pixel)

def get_random_position(image):
    return (random.randint(0, image.width - 1), random.randint(0, image.height - 1))

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('samples', help='location of samples')
    parser.add_argument('-o', '--output', help='location of generated output', default='generated.png')
    parser.add_argument('-x', '--width', type=int, help='width of generated output', default=1920)
    parser.add_argument('-y', '--height', type=int, help='height of generated output', default=1080)
    parser.add_argument('-i', '--invert', action='store_true', help='Invert the image color')
    args = parser.parse_args()

    samples_dir = Path(args.samples)
    assert samples_dir.is_dir(), f"{samples_dir} is not a directory"
    sample_names = glob.glob(str(samples_dir / '*.png'))
    samples = get_samples(sample_names)

    output = Image.new(mode='RGB', size=(args.width, args.height), color=(255, 255, 255))

    for sample in samples:
        for i in range(10):
            pos = get_random_position(output)
            place_sample(output, sample, pos)

    if args.invert:
        output = ImageOps.invert(output)

    output.save(args.output)

if __name__ == '__main__':
    main()
