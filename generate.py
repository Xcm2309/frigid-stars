import png
import random
import math
import numpy as np

row_count = 1080
col_count = 1920

channel_red = 0
channel_green = 1
channel_blue = 2
channel_alpha = 3
channels = 4

image_width = 0
image_height = 1
image_values = 2

def getSolidColorImage(red, green, blue, alpha):
    image_3d = np.zeros(shape=(row_count, col_count, channels), dtype=np.uint16)

    for row in range(row_count):
        for col in range(col_count):
            image_3d[row][col][channel_red] = red
            image_3d[row][col][channel_green] = green
            image_3d[row][col][channel_blue] = blue
            image_3d[row][col][channel_alpha] = alpha

    return image_3d

def getRandomPointCircle(radius=0):
    angle = 2 * math.pi * random.random()
    length = random.random()
    
    x_pos = round(radius * length * math.cos(angle)) + radius
    y_pos = round(radius * length * math.sin(angle)) + radius
    return (x_pos, y_pos)

def getRandomPoint(width, height):
    x_pos = round(width * random.random())
    y_pos = round(height * random.random())
    return (x_pos, y_pos)

def isDarker(pixel1, pixel2):
    pixel1_brightness = (int(pixel1[0]) + int(pixel1[1]) + int(pixel1[2])) / 3
    pixel2_brightness = (int(pixel2[0]) + int(pixel2[1]) + int(pixel2[2])) / 3

    return pixel1_brightness < pixel2_brightness

def getSamples(num_samples):
    images = []
    for i in range(num_samples):
        r=png.Reader(filename="samples/sample" + str(i) + ".png").read_flat()
        image_2d = r[image_values]
        image_3d = np.reshape(image_2d, (r[image_height], r[image_width], channels))
        images.append(image_3d)
    return images

def getImageWidth(image):
    return len(image[0])

def getImageHeight(image):
    return len(image)

def invertColors(image):
    for i in range(getImageHeight(image)):
        for j in range(getImageWidth(image)):
            image[i][j][channel_red] = 255 - image[i][j][channel_red]
            image[i][j][channel_green] = 255 - image[i][j][channel_green]
            image[i][j][channel_blue] = 255 - image[i][j][channel_blue]

num_samples = 300
images = getSamples(num_samples)
image_3d = getSolidColorImage(255, 255, 255, 255)

for i in range(1000):
    x_pos, y_pos = getRandomPoint(1920,1080)
    random_sample = int(num_samples * random.random())
    for j in range(getImageHeight(images[random_sample])):
        for k in range(getImageWidth(images[random_sample])):
            if (y_pos + j) < row_count and (x_pos + k) < col_count: 
                if isDarker(images[random_sample][j][k], image_3d[y_pos + j][x_pos + k]):
                    image_3d[y_pos + j][x_pos + k][0] = images[random_sample][j][k][0]
                    image_3d[y_pos + j][x_pos + k][1] = images[random_sample][j][k][1]
                    image_3d[y_pos + j][x_pos + k][2] = images[random_sample][j][k][2]
                    image_3d[y_pos + j][x_pos + k][3] = images[random_sample][j][k][3]


#invertColors(image_3d)
image_2d = np.reshape(image_3d, (-1, col_count * channels)).tolist()
f = open('test.png', 'wb')
w = png.Writer(height=row_count, width=col_count, greyscale=False, alpha=True)
w.write(f, image_2d)
f.close()

