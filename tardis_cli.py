import time
import random

from rpi_ws281x import Color, ws
from models import TARDIS

BLUE = Color(0, 0, 255)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
PURPLE = Color(127, 0, 255)
YELLOW = Color(255, 255, 0)
GREEN = Color(50, 205, 50)
TEAL = Color(100, 128, 128)
NAVY = Color(0, 0, 128)
LIGHTRED = Color(5, 0, 0)
TARDISBLUE = Color(0, 59, 111)
GRAY = Color(66, 66, 66)


def rgb_int2tuple(rgbint):
    return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def colorFill(strip, color, wait_ms=100):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms / 1000.0)


def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return Color(r, g, b)


# Main program logic follows:
if __name__ == "__main__":
    myTARDIS = TARDIS("Mike Nibeck", TARDISBLUE)
    # myTARDIS.frontWindow.pulse(2, 0.001)
    time.sleep(1)

    myTARDIS.setWindowColors(random_color_generator())
    time.sleep(0.5)
    myTARDIS.setWindowColors(random_color_generator())
    time.sleep(0.5)
    myTARDIS.setWindowColors(random_color_generator())
    time.sleep(0.5)
    myTARDIS.setWindowColors(random_color_generator())
    time.sleep(0.5)
    myTARDIS.turnOff()

    # rainbowCycle(strip)
    # theaterChaseRainbow(strip)
    # colorWipe(strip, Color(0, 0, 0))
