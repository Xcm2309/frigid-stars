import argparse
import glob
from pathlib import Path
from PIL import Image, ImageOps
import random


def get_samples(sample_names):
    '''Returns a list of images opened from sample_names'''
    samples = []
    for sample_name in sample_names:
        sample = Image.open(sample_name)
        samples.append(sample)
    return samples


def is_darker(pixel1, pixel2):
    '''Returns True if pixel1 is darker than pixel2.'''
    return sum(pixel1[:3]) < sum(pixel2[:3])


def pixel_within_bounds(position, image):
    '''Returns True if position is within the bounds of image.'''
    return position[0] >= 0 and position[0] < image.width and position[1] >= 0 and position[1] < image.height


def place_sample(image, sample, position):
    '''Places sample onto image at position.

    This function will only write a pixel of sample to image if the sample pixel
    is darker than the position on image.
    '''
    for x in range(sample.width):
        for y in range(sample.height):
            image_position = (position[0] + x, position[1] + y)
            if pixel_within_bounds(image_position, image):
                sample_pixel = sample.getpixel((x, y))
                image_pixel = image.getpixel(image_position)

                if is_darker(sample_pixel, image_pixel):
                    image.putpixel(image_position, sample_pixel)


def get_random_position(image):
    '''Returns a random position in the given image to place a sample.

    The top left corner of the sample is placed at the position so 50 pixels
    of scratch space is given to create a more natural looking generated image.
    '''
    return (random.randint(-50, image.width + -1), random.randint(-50, image.height - 1))


def main():
    parser = argparse.ArgumentParser(description='Generate a frigid stars image')
    parser.add_argument('-i', '--invert', action='store_true', help='Invert the image color')
    parser.add_argument('-n', '--num-samples', type=int, help='The number of samples to place in the output', default=2000)
    parser.add_argument('-o', '--output', type=str, help='Path of generated output', default='generated.png')
    parser.add_argument('-s', '--samples', type=str, help='Path of samples', default='samples')
    parser.add_argument('-x', '--width', type=int, help='Width of generated output', default=1920)
    parser.add_argument('-y', '--height', type=int, help='Height of generated output', default=1080)
    args = parser.parse_args()

    samples_dir = Path(args.samples)
    assert samples_dir.is_dir(), f"{samples_dir} is not a directory"
    sample_names = glob.glob(str(samples_dir / '*.png'))
    samples = get_samples(sample_names)

    output = Image.new(mode='RGB', size=(args.width, args.height), color=(255, 255, 255))

    for _ in range(args.num_samples):
        pos = get_random_position(output)
        sample = samples[random.randint(0, len(samples) - 1)]
        place_sample(output, sample, pos)

    if args.invert:
        output = ImageOps.invert(output)

    output.save(args.output)


if __name__ == '__main__':
    main()
