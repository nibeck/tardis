#include all necessary packages to get LEDs to work with Raspberry Pi
import time
import math
from rpi_ws281x import *
import argparse
import colorsys
from tardis import TARDIS

BLUE    = Color(0,0,255)
BLACK   = Color(0,0,0)
WHITE   = Color(255,255,255)
RED     = Color(255,0,0)
PURPLE  = Color(127,0,255)
YELLOW  = Color(255,255,0)
GREEN   = Color(50,205,50)
TEAL    = Color(100,128,128)
NAVY    = Color(0,0,128)

def fadeWindow(window, delay, cycles):
    brightnessPercentage = 100
    startColor = window.color
    startR = startColor.r 
    startG = startColor.g 
    startB = startColor.b 

    while window.color != BLACK:
        window.setBrightness(brightnessPercentage)
        brightnessPercentage = brightnessPercentage - 1
        myTARDIS.backWindow.updateLEDs()
        time.sleep(delay)
    brightnessPercentage = 100    
    while window.color != startColor:
        window.setBrightness(brightnessPercentage)
        brightnessPercentage = brightnessPercentage + 1
        
        myTARDIS.backWindow.updateLEDs()
        time.sleep(delay)

def rgb_to_hls1(rgb_color):
    # Ensure that the RGB values are in the range [0, 255]
    r, g, b = [min(255, max(0, int(x))) for x in rgb_color]

    # Normalize RGB values to the range [0, 1]
    r_normalized = r / 255.0
    g_normalized = g / 255.0
    b_normalized = b / 255.0

    # Convert RGB to HLS
    h, l, s = colorsys.rgb_to_hls(r_normalized, g_normalized, b_normalized)

    # Convert hue to degrees (0-360)
    h_degrees = int(h * 360)

    return {
        'rgb': (r, g, b),
        'hls': (h_degrees, l, s),
        'hue': h_degrees,
        'saturation': s,
        'luminance': l
    }

def rgb_to_hls(r, g, b):
    # Ensure that the RGB values are in the range [0, 255]
    r = min(255, max(0, int(r)))
    g = min(255, max(0, int(g)))
    b = min(255, max(0, int(b)))

    # Normalize RGB values to the range [0, 1]
    r_normalized = r / 255.0
    g_normalized = g / 255.0
    b_normalized = b / 255.0

    # Convert RGB to HLS
    h, l, s = colorsys.rgb_to_hls(r_normalized, g_normalized, b_normalized)

    # Convert hue to degrees (0-360)
    h_degrees = int(h * 360)

    return h_degrees, s, l

def colorConversionTest():

    r = 0
    g = 0
    b = 128
    print('RGB:-')
    print('r: ' + str(r) + '\ng: ' + str(g) + '\nb: ' + str(b))
    ## normalizing values to get value between 0 and 1
    r = r/255
    g = g/255
    b = b/255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    print('Normalized RGB:-')
    print('r: ' + str(r) + '\ng: ' + str(g) + '\nb: ' + str(b))
    print('\nHLS:-')
    print('h: ' + str(h) + '\nl: ' + str(l) + '\ns: ' + str(s))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    print('\nRGB:-')
    print('r: ' + str(r) + '\ng: ' + str(g) + '\nb: ' + str(b))
    r = r * 255
    g = g * 255
    b = b * 255
    print('\nNormalized RGB:-')
    print('r: ' + str(r) + '\ng: ' + str(g) + '\nb: ' + str(b))

def pulseLightness(delay):
    # HLS: Hue, lightnmess, saturation
    normalizedRed = myTARDIS.backWindow.color.r / 255
    normalizedGreen = myTARDIS.backWindow.color.g / 255
    normalizedBlue = myTARDIS.backWindow.color.b / 255
    hue, lightness, saturation = colorsys.rgb_to_hls(normalizedRed, normalizedGreen, normalizedBlue)

    while True:
        for lightness in range(1, 101):
            # convert back to rgb usinf hls with inctreased lightness
            newR, newG, newB = colorsys.hls_to_rgb(hue, lightness/100, saturation) 
            # normalize new RGB valies from the HLS conversion and set new color with increased limunance
            newR = newR * 255
            newG = newG * 255
            newB = newB * 255
            
            # set the new color of the window
            adjustedColor = Color(math.trunc(newR), math.trunc(newG), math.trunc(newB))
            myTARDIS.backWindow.setColor(adjustedColor)
            time.sleep(delay)
        for lightness in range(100, 1, -1):
            # convert back to rgb using hls with inctreased lightness
            newR, newG, newB = colorsys.hls_to_rgb(hue, lightness/100, saturation) 
            # normalize new RGB valies from the HLS conversion and set new color with increased limunance
            newR = newR * 255
            newG = newG * 255
            newB = newB * 255
            
            # set the new color of the window
            adjustedColor = Color(math.trunc(newR), math.trunc(newG), math.trunc(newB))
            myTARDIS.backWindow.setColor(adjustedColor)
            time.sleep(delay)


myTARDIS = TARDIS("Mike Nibeck", BLUE)
myTARDIS.backWindow.setColor(BLUE)
# myTARDIS.turnOn
print(myTARDIS.backWindow.color.r, myTARDIS.backWindow.color.g, myTARDIS.backWindow.color.b)
print("Backwindow brightness: ", myTARDIS.backWindow.brightness)
# myTARDIS.backWindow.setColor(RED)
time.sleep(1)
# myTARDIS.backWindow.setBrightness(50)
time.sleep(1)

# myTARDIS.backWindow.flash(5, .1)
# myTARDIS.backWindow.pulseWindow(.005, 2)
# myTARDIS.frontWindow.setColor(blue, 100)
# myTARDIS.frontWindow.pulseWindow(.005, 2)

time.sleep(1)
myTARDIS.turnOff()