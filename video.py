#!/usr/bin/python
# coding=utf-8

import time,os,sys, time, signal, pygame

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

print("终端模式下，你可以按下ctrl+c键结束程序")

def signal_handler(signal, frame):
    print("\n你摁下了Ctrl+C!程序结束")
    pygame.mixer.music.stop()
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

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

# 12864.mp4 128*64 24帧，无音频

video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '12864.mp4'))
print('Loading {}...'.format(video_path))

clip = av.open(video_path)

pygame.init()
track = pygame.mixer.music.load('12864.mp3')
pygame.mixer.music.play()
# 加载音频


for frame in clip.decode(video=0):
    starttime = time.time() # 记录开始时间

    print('{} ------'.format(frame.index))

    # print(format(frame.index))

    imgs = frame.to_image() ## 提取视频帧
    # img = imgs.resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')  ## 将图片分辨率调整为屏幕大小，色彩1bit
    img = imgs.convert('1')  ##色彩1bit
    disp.image(img)
    disp.display()

    endtime = time.time() #结束时间
    times = endtime - starttime #显示该帧所用时间
    timec = round(times,3)
    print(timec),

    if(timec < 0.040): #该视频为24帧,每帧所用时间1/24=0.041,如果小于0.041则暂停,以免播放过快
        print(0.040-timec) # 测试后发现每帧0.04秒最佳
        time.sleep(0.040-timec)

    endtimes = time.time()
    print(endtimes - starttime)

