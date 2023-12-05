"""
ESP32-DevKitC V4/MicroPython exercise
240x240 ST7789 SPI LCD
using MicroPython library:
https://github.com/russhughes/st7789py_mpy

"""

import uos
import machine
import st7789py as st7789
from fonts import vga1_16x32 as font
import random
import ustruct as struct
import utime

"""
ST7789 Display  ESP32-DevKitC (SPI2)
SCL             GPIO13
SDA             GPIO11
                GPIO19  (miso not used)

ST7789_rst      GPIO5
ST7789_dc       GPIO4
"""
#ST7789 use SPI(2)

st7789_res = 5
st7789_dc  = 4
pin_st7789_res = machine.Pin(st7789_res, machine.Pin.OUT)
pin_st7789_dc = machine.Pin(st7789_dc, machine.Pin.OUT)

disp_width = 240
disp_height = 280
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)

print(uos.uname())
#spi2 = machine.SPI(2, baudrate=40000000, polarity=1)
pin_spi2_sck = machine.Pin(13, machine.Pin.OUT)
pin_spi2_mosi = machine.Pin(11, machine.Pin.OUT)
pin_spi2_miso = machine.Pin(19, machine.Pin.IN)
spi2 = machine.SPI(2, sck=pin_spi2_sck, mosi=pin_spi2_mosi, miso=pin_spi2_miso,
                   baudrate=40000000, polarity=1, phase=0, bits=8)
print(spi2)

display = st7789.ST7789(spi2, disp_width, disp_width,
                          reset=pin_st7789_res,
                          dc=pin_st7789_dc,
                          xstart=0, ystart=0, rotation=0)

print(display)

display.fill(st7789.BLACK)
display.text(font, "Hello!", 20, 20)
display.text(font, "ESP32", 20, 50)
display.text(font, "MicroPython", 20, 80)
display.text(font, "ST7789 SPI", 20, 110)
display.text(font, "240*280 IPS", 20, 180)


