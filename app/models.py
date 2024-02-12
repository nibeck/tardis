import time, math, random
from rpi_ws281x import Color, PixelStrip
import colorsys

# setup some comnstants
LED_COUNT = 40  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
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


def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return Color(r, g, b)


class TARDIS:
    def __init__(self, doctor, color):
        self.doctor = doctor if doctor is not None else ""
        self.color = color if color is not None else TARDISBLUE
        # Create the 4 Windows

        self.frontWindow = self.Window()
        self.frontWindow.location = "front"
        self.frontWindow.color = GRAY
        self.frontWindow.prevColor = self.frontWindow.color
        self.frontWindow.brightness = 50

        self.backWindow = self.Window()
        self.backWindow.location = "back"
        self.backWindow.color = GRAY
        self.backWindow.prevColor = self.backWindow.color
        self.backWindow.brightness = 50

        self.rtWindow = self.Window()
        self.rtWindow.location = "right"
        self.rtWindow.color = GRAY
        self.rtWindow.prevColor = self.rtWindow.color
        self.rtWindow.brightness = 50

        self.leftWindow = self.Window()
        self.leftWindow.location = "left"
        self.leftWindow.color = GRAY
        self.leftWindow.prevColor = self.leftWindow.color
        self.leftWindow.brightness = 50

        # top Light
        self.topLightColor = GRAY
        self.topLightPrevColor = self.topLightColor
        self.topLightBrightness = 50
        self.topLightPrevBrioghtness = self.topLightBrightness

    def turnOff(self):
        self.frontWindow.turnOff()
        self.backWindow.turnOff()
        self.rtWindow.turnOff()
        self.leftWindow.turnOff()

    def turnOn(self):
        self.frontWindow.turnOn()
        self.backWindow.turnOn()
        self.rtWindow.turnOn()
        self.leftWindow.turnOn()

    def rainbow(self):
        self.frontWindow.setColor(RED)
        self.backWindow.setColor(PURPLE)
        self.rtWindow.setColor(TEAL)
        self.leftWindow.setColor(NAVY)

    def randomColors(self):
        self.frontWindow.randomColor()
        self.backWindow.randomColor()
        self.rtWindow.randomColor()
        self.leftWindow.randomColor()

    def setWindowColors(self, newColor):
        self.frontWindow.color = newColor
        self.backWindow.color = newColor
        self.rtWindow.color = newColor
        self.leftWindow.color = newColor

    class Window:
        def __init__(self):
            self._color = WHITE
            self.prevColor = BLACK
            self._brightness = 50
            self.prevBrightness = 0

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, new_color):
            self.prevColor = self.color
            self._color = new_color
            self.updateLED_color()

        @property
        def brightness(self):
            return self._brightness

        @brightness.setter
        def brightness(self, new_brightness):
            # print("In brightness setter")

            # ensure brightness apssed in is betwen 0 and 100
            new_brightness = max(min(new_brightness, 100), 0)

            # Perform linear mapping - map to 0-50 (50=maximum brightness)
            # allow user to pass in 100 as max as that feels more normal.
            # do this mapping internally to increase ease of use
            #       (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
            mapped_brightness = (new_brightness - 0) * (50 - 1) / (100 - 0) + 1
            # Round the result to an integer (optional, depending on your needs)
            mapped_brightness = int(round(mapped_brightness))

            # normalize RGB valies of the current color to prepare for the hls conversion
            normalizedRed = self.color.r / 255
            normalizedGreen = self.color.g / 255
            normalizedBlue = self.color.b / 255

            # convert RGB values into HlS values, so we can extract the "lightness" of the current color
            hue, origLightness, saturation = colorsys.rgb_to_hls(
                normalizedRed, normalizedGreen, normalizedBlue
            )
            if mapped_brightness == 0:
                mapped_brightness = 1

            # convert back to rgb using hls with new brightness values passed in (divide by 100 to put it inhls range (.1-1.0)
            newR, newG, newB = colorsys.hls_to_rgb(
                hue, mapped_brightness / 100, saturation
            )
            # normalize new RGB valies from the HLS conversion, so we can cobert back to RBG, which the LEDs need
            newR = newR * 255
            newG = newG * 255
            newB = newB * 255

            # set the new color of the window
            adjustedColor = Color(math.trunc(newR), math.trunc(newG), math.trunc(newB))

            self.color = adjustedColor
            self.prevBrightness = self.brightness
            # set property directly, so you don't trigger this setter method and create a loop
            self._brightness = new_brightness

            globalLightStrip.show()

        @property
        def location(self):
            return self._location

        @location.setter
        def location(self, new_location):
            self._location = new_location
            match self._location:
                case "front":
                    self.ledIndices = range(10)  # 0-9
                case "right":
                    self.ledIndices = range(10, 19, 1)  # 10-19
                case "left":
                    self.ledIndices = range(20, 29, 1)  # 20-29
                case "back":
                    self.ledIndices = range(30, 39, 1)  # 30-39
                case _:
                    raise ValueError("Location must be front, right, back, left")

        def __str__(self):
            return "Window Color {} : PrevColor {} : Brightness {} : PrevBrightness {} : Location {}".format(
                rgb_int2tuple(self.color),
                rgb_int2tuple(self.prevColor),
                self.brightness,
                self.prevBrightness,
                self.location,
            )

        def turnOn(self):
            self._brightness = self.prevBrightness
            self.color = self.prevColor
            self.prevColor = BLACK
            self.updateLED_color()

        def turnOff(self):
            self.prevColor = self.color
            self.prevBrightness = self.brightness
            self.color = BLACK
            self.updateLED_color()

        def updateLED_color(self):
            for ix in self.ledIndices:
                globalLightStrip.setPixelColor(ix, self.color)
            globalLightStrip.show()

        def flash(self, cycles, delay):
            # Save state
            currentColor = self.color
            currentBrightness = self.brightness
            for n in range(cycles):
                time.sleep(delay)
                self.turnOff()
                time.sleep(delay)
                self.turnOn()
                # print(self)
            self.brightness = currentBrightness
            self.color = currentColor

        def pulse(self, cycles, delay):
            # save starting point so we can return to it
            starting_Brightness = self.brightness
            starting_Color = self.color
            # print("Starting color-brightness - ", starting_Color, starting_Brightness)
            # iterate through changing brightness as we go
            for cycles in range(cycles):
                # start at current brightness and go down to 1 (don't go to 0 as it will flip color to white)
                for newbrightness in range(starting_Brightness, 1, -1):
                    self.brightness = newbrightness
                    # self.turnOn()
                    # print("Brightness: ", newbrightness)
                    time.sleep(delay)
                for newbrightness in range(1, starting_Brightness, 1):
                    # print("Brightness: ", newbrightness)
                    self.brightness = newbrightness
                    # self.turnOn()
                    time.sleep(delay)
            self.color = starting_Color
            self._brightness = starting_Brightness
            self.updateLED_color()

        def randomColor(self):
            self.color = random_color_generator()

        # class Sign:
        # def __init__(self, color, brightness):
        #     self.color = color if color is not None else Color(0.0, 0)
        #     self.brightness = brightness if brightness is not None else 0


# Create NeoPixel object with appropriate configuration.
globalLightStrip = PixelStrip(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
)

# Intialize the library (must be called once before other functions).
globalLightStrip.begin()
