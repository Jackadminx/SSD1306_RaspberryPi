#!/usr/bin/python
# coding=utf-8

import time,os

import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_SSD1306

from PIL import Image


import av
from av.frame import Frame
from av.packet import Packet
from av.stream import Stream
from av.utils import AVError
from av.video import VideoFrame



# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Load image based on OLED display height.  Note that image is converted to 1 bit color.
# if disp.height == 64:
#     image = Image.open('happycat_oled_64.ppm').convert('1')
# else:
#     image = Image.open('happycat_oled_32.ppm').convert('1')

image = Image.open('test.png').convert('1')


# Alternatively load a different format image, resize it, and convert to 1 bit color.
#image = Image.open('happycat.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')

# Display image.
disp.image(image)
disp.display()

time.sleep(1)



video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'A.mp4'))
print('Loading {}...'.format(video_path))

clip = av.open(video_path)

for frame in clip.decode(video=0):
    print('{} ------'.format(frame.index))
    imgs = frame.to_image() ## 提取视频帧
    img = imgs.resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')  ## 将图片分辨率调整为屏幕大小，色彩1bit
    disp.image(img)
    disp.display()

