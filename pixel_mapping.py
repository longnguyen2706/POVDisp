from collections import Counter
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import copy

NUM_LEDS = 10
IMAGE_SIZE = NUM_LEDS *2

def read_image(image_dir):
    image = cv2.imread(image_dir)
    return image

def resize_image(image):
    return cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_CUBIC)

def convert_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def convert_to_binary(image):
    ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def show_image(image, title):
    plt.subplot(1, 1, 1), plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.xticks([]), plt.yticks([])
    plt.show()

def convert_to_cardesian(image):
    (height, width) = image.shape
    cardesian_img = []
    for x in range (0, width):
        for y in range (0, height):
            pixel = CardesianPixel()
            pixel.x = int(x-width/2) if x< width/2 else int(x-width/2+1)
            pixel.y = int(y-height/2) if y<height/2 else int(y-height/2+1)
            pixel.value = image[x][y]
            cardesian_img.append(pixel)

    for x in range (0, width+1):
        pixel = CardesianPixel()
        pixel.x = int(x-width/2)
        pixel.y = 0
        pixel.value = 0
        cardesian_img.append(pixel)

    for y in range (0, height+1):
        pixel = CardesianPixel()
        pixel.y = int(y - height/2)
        pixel.x = 0
        pixel.value = 0
        cardesian_img.append(pixel)

    print('unsorted', cardesian_img)
    cardesian_img.sort(key=lambda p: p.x)
    print('sorted x', cardesian_img)

    cardesian_img.sort(key=lambda p: p.y)
    print('sorted y', cardesian_img)

    return cardesian_img

def convert_to_polar(cardesian_img):
    polar_img = []
    for p in cardesian_img:
        pixel = PolarPixel()
        # pixel.r = np.sqrt(p.x*p.x + p.y*p.y)
        # pixel.theta = np.arctan2(p.y, p.x)*180/math.pi
        (pixel.r, pixel.theta) = cart2pol(p.x, p.y, True)
        pixel.value = p.value
        polar_img.append(pixel)

    print('polar_img', polar_img)
    return polar_img

def pol2cart(r, theta, is_int=False):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    if is_int:
        x = int(x)
        y = int(y)
    return (x, y)

def cart2pol(x, y, is_deg=False):
    r = np.sqrt(x **2 + y** 2)
    theta = np.arctan2(y, x)
    if is_deg:
        theta = theta*180/math.pi
    return (r, theta)

def displayable_pixels(deg):
    # for x in range (0, IMAGE_SIZE+1):
    #     for y in range (0, IMAGE_SIZE+1):
    displayable_pixels=[]
    num_segs = int(360/deg)
    for i in range (0, num_segs):
        for l in range (1, NUM_LEDS+1):
            (x,y) = pol2cart(l, i*deg*math.pi/180, True)
            displayable_pixels.append((x,y))

    # print("displayable pixels", displayable_pixels)
    print (Counter(displayable_pixels).keys())
    print (Counter(displayable_pixels).values())
    print (len(Counter(displayable_pixels).keys()))
    return displayable_pixels

def displayable_region(displayable_pixels):
    img_region = np.zeros((IMAGE_SIZE+1, IMAGE_SIZE+1))
    for (x, y) in displayable_pixels:
        x_cord = x + int(IMAGE_SIZE/2)
        y_cord = y + int(IMAGE_SIZE/2)
        img_region[x_cord][y_cord] = 255

    return img_region

def displayale_img(cardesian_img, displayable_pixels):
    img = np.zeros((IMAGE_SIZE+1, IMAGE_SIZE+1))
    for (x, y) in displayable_pixels:
        for pixel in cardesian_img:
            x_cord = x + int(IMAGE_SIZE / 2)
            y_cord = y + int(IMAGE_SIZE / 2)
            if (x == pixel.x and y == pixel.y):
                img[x_cord][y_cord] = pixel.value
    return img

def img_to_led_disp(cardesian_img, deg):
    led_strip_data = []
    num_segs = int(360 / deg)
    data_to_map = copy.copy(cardesian_img)
    for i in range(0, num_segs):
        led_strip = []
        for l in range(1, NUM_LEDS + 1):
            l_val = 0
            (x, y) = pol2cart(l, i * deg * math.pi / 180, True)
            for pixel in data_to_map:
                if (x == pixel.x and y == pixel.y):
                    if pixel.value == 255:
                        l_val = 1
                    data_to_map.remove(pixel)
            led_strip.append(l_val)
        led_strip_data.append(led_strip)
        
    print("led strip data", led_strip_data)
    return led_strip_data

class CardesianPixel():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.value = 0

    def __repr__(self):
        return "<(x, y, val): %s, %s, %s> \n" % (self.x, self.y, self.value)

class PolarPixel():
    def __init__(self):
        self.r = 0
        self.theta = 0
        self.value =0

    def __repr__(self):
        return "<(r, theta, val): %s, %s, %s>\n" % (self.r, self.theta, self.value)

img = read_image('/home/long/Documents/POVBike/Simulator/logo.png')
show_image(img, 'original image')

img_resized = resize_image(img)
show_image(img_resized, 'resized image')

img_gray = convert_to_gray(img_resized)
show_image(img_gray, 'gray image')

img_binary = convert_to_binary(img_gray)
show_image(img_binary, 'binary image')

cardesian_img = convert_to_cardesian(img_binary)
polar_img = convert_to_polar(cardesian_img)

displayable_pixels = displayable_pixels(10)
displayable_region = displayable_region(displayable_pixels)
show_image(displayable_region, 'displayable region')

displayable_img = displayale_img(cardesian_img, displayable_pixels)
show_image(displayable_img, 'displayable image')

img_to_led_disp(cardesian_img, 10)