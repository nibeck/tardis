import time
import math
from rpi_ws281x import *
import colorsys

# TODO: Expose as restful services
# TODO: redo get() set() properly for tardis oject

#setup some comnstants
LED_COUNT      = 40         # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
BLUE    = Color(0,0,255)
BLACK   = Color(0,0,0)
WHITE   = Color(255,255,255)
RED     = Color(255,0,0)
PURPLE  = Color(127,0,255)
YELLOW  = Color(255,255,0)
GREEN   = Color(50,205,50)
TEAL    = Color(100,128,128)
NAVY    = Color(0,0,128)

class TARDIS:
    def __init__(self, doctor, color):
        self.doctor = doctor if doctor is not None else ""
        self.color = color if color is not None else Color(0,0,0) 
        # Create the 4 Windows
        self.frontWindow = Window()
        self.frontWindow.location = "front"
        self.frontWindow.color = Color(0,0,0)
        # self.frontWindow.brightness = 50

        self.backWindow = Window()
        self.backWindow.location = "back"
        self.backWindow.color = Color(0,0,0)
        # self.backWindow.brightness = 50

        self.rtWindow = Window()
        self.rtWindow.location = "right"
        self.rtWindow.color = Color(0,0,0)
        # self.rtWindow.brightness = 50

        self.leftWindow = Window()
        self.leftWindow.location = "left"
        self.leftWindow.color = Color(0,0,0)
        # self.leftWindow.brightness = 50

        # Create the 4 Signs
        # TODO: Replace getters/setters with property
        self.frontSign = Sign(Color(255,255,255), 0)
        self.backSign = Sign(Color(255,255,255), 0)
        self.rtSign = Sign(Color(255,255,255), 0)
        self.leftSign = Sign(Color(255,255,255), 0)
        # top Light
        self.topLightClor = Color(0,0,0)
        self.topLightBrightness = 0

        # initialize light strip
        self.lightStrip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.lightStrip.begin()
        
    def turnOff(self):
        self.frontWindow.turnOff()
        self.backWindow.turnOff()
        self.rtWindow.turnOff()
        self.leftWindow.turnOff()
    
    def turnOn(self):
        self.frontWindow.setColor(WHITE)
        self.backWindow.setColor(WHITE)
        self.rtWindow.setColor(WHITE)
        self.leftWindow.setColor(WHITE)
    
    def rainbow(self):
        self.frontWindow.setColor(RED)
        self.backWindow.setColor(PURPLE)
        self.rtWindow.setColor(TEAL)
        self.leftWindow.setColor(NAVY)
    
    def flash(self):
            self.backSign

class Window:
    def __init__(self):
        self._color = Color(0,0,0)
        self._brightness = 50

    @property
    def color(self):
        return self._color
    @color.setter    
    def color(self, new_color):
        self._color = new_color
        self.updateLED_color()

    @property
    def brightness(self):
        return self._brightness    
    @brightness.setter
    def brightness(self, new_brightness):
        # ensure brightness apssed in is betwen 0 and 100
        new_brightness = max(min(new_brightness, 100), 0)
    
        # Perform linear mapping - map to 0-50 (50=maximum brightness)
        # allow user to pass in 100 as max as that feels more normal. 
        # do this mapping interannly to increase ease of use
        #       (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min        
        mapped_value = (new_brightness - 0) * (50 - 1) / (100 - 0) + 1
        # Round the result to an integer (optional, depending on your needs)
        mapped_value = int(round(mapped_value))

        # nromalize RGB valies to prepare for the hls conversion
        normalizedRed = self.color.r / 255
        normalizedGreen = self.color.g / 255
        normalizedBlue = self.color.b / 255

        # convert RGB valiues into Hls values
        hue, origLightness, saturation = colorsys.rgb_to_hls(normalizedRed, normalizedGreen, normalizedBlue)
        # convert back to rgb usinf hls with new brightness values passed in (divide by 100 to put it inhls range (.1-1.0)
        newR, newG, newB = colorsys.hls_to_rgb(hue, mapped_value/100, saturation)
        # normalize new RGB valies from the HLS conversion 
        newR = newR * 255
        newG = newG * 255
        newB = newB * 255

        # set the new color of the window
        adjustedColor = Color(math.trunc(newR), math.trunc(newG), math.trunc(newB))
        self.color = adjustedColor
        lightStrip.show()
        self._brightness = new_brightness

    @property
    def location(self):
        return self._location
    @location.setter
    def location(self, new_location):
        self._location = new_location
        match self._location:
            case "front":
                self.ledIndices = range(10)        #0-9
            case "right":
                self.ledIndices = range(10, 19, 1) #10-19
            case "left":
                self.ledIndices = range(20, 29, 1) #20-29
            case "back":
                self.ledIndices = range(30, 39, 1) #30-39
            case _:
                raise ValueError("Location must be front, right, back, left")

    def __str__(self):
        return "Color: {} Brightness: {} Location: {}".format(self.color, self.brightness, self.location)

    def turnOn(self):
        lightStrip.show()
    
    def turnOff(self):   
        # Todo: Change to set to 0% brightness onmce brightness is working
        self.color = Color(0,0,0)
        self.updateLED_color()
        lightStrip.show()
    
    def updateLED_color(self):
        for ix in self.ledIndices:
            lightStrip.setPixelColor(ix, self.color)    
        # lightStrip.show()

    def flash(self, cycles, delay):
        origColor = self.color
        for n in range(cycles):
            time.sleep(delay)
            self.color = origColor
            lightStrip.show()
            time.sleep(delay)
            self.brightness = 0
            lightStrip.show()
        self.color = origColor

    def pulseWindow(self, cycles, delay):
            # save starting point so we can return to it
            starting_brightness = self.brightness
            # iterate through changing brightness as we go
            for cycles in range(cycles):
                # start at current brightness and go down to 0
                for newbrightness in range(starting_brightness, 1, -1):
                    self.brightness = newbrightness
                    self.turnOn()
                    time.sleep(delay)
                for newbrightness in range(1, starting_brightness, 1):
                    self.brightness = newbrightness
                    self.turnOn()
                    time.sleep(delay)

class Sign:
    def __init__(self, color, brightness):
        self.color = color if color is not None else Color(0.0,0)
        self.brightness = brightness if brightness is not None else 0

# Create NeoPixel object with appropriate configuration.
lightStrip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Intialize the library (must be called once before other functions).
lightStrip.begin()
