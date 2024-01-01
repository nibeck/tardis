import time
import math
from rpi_ws281x import *
import colorsys

class TARDIS:
    def __init__(self, doctor, color):
        self.doctor = doctor if doctor is not None else ""
        self.color = color if color is not None else Color(0,0,0) 
        # Windows
        self.frontWindow = window("front", Color(255,255,255), 50)
        self.backWindow = window("back", Color(255,255,255), 50)
        self.rtWindow = window("right", Color(255,255,255), 50)
        self.leftWindow = window("left", Color(255,255,255), 50)
        # Signs
        self.frontSign = sign(Color(255,255,255), 0)
        self.backSign = sign(Color(255,255,255), 0)
        self.rtSign = sign(Color(255,255,255), 0)
        self.leftSign = sign(Color(255,255,255), 0)
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
        self.frontWindow.turnOn()
        self.backWindow.turnOn()
        self.rtWindow.turnOn()
        self.leftWindow.turnOn()

class window:
    def __init__(self, location, color, brightness):
        self.color = color if color is not None else Color(255,255,255)
        self.location = location if location is not None else "front"
        self.brightness = brightness if brightness is not None else 50
        # add logic to look at location and properly set a new attribute called LEDindex to the approate indices.
        match self.location:
            case "front":
                self.ledIndices = range(10)        #0-9
            case "right":
                self.ledIndices = range(10, 19, 1) #10-19
            case "left":
                self.ledIndices = range(20, 29, 1) #20-29
            case "back":
                self.ledIndices = range(30, 39, 1) #30-39

    def __str__(self):
        return "Color: {} Brightness: {} Location: {}".format(self.color, self.brightness, self.location)

    def turnOn(self):
        self.updateLEDs()
    
    def turnOff(self):   
        self.setBrightness(0)
        self.updateLEDs()
    
    def updateLEDs(self):
        for ix in self.ledIndices:
            lightStrip.setPixelColor(ix, self.color)    
        lightStrip.show()

    def setBrightness(self, percentage):
        # clamp brightness percentage into 0-100 range
        percentage = min(100, max(0, percentage))

        # HSV: hue, saturation, value (0-255)
        # normalize RGB valeue top work with HSV by dividing by 255
        hue, saturation, colorValue = colorsys.rgb_to_hsv((self.color.r / 255), (self.color.g / 255), (self.color.b / 255) )
        colorValue = colorValue * (percentage / 100)

        # get new RGB valiues
        newR, newG, newB = colorsys.hsv_to_rgb(hue, saturation, colorValue)

        # set the new color of the window
        # normalize the returned RGB value by multieplying by 255
        adjustedColor = Color(math.trunc(newR*255), math.trunc(newG*255), math.trunc(newB*255))
        self.setColor(adjustedColor)
        self.brightness = percentage
        self.updateLEDs()

    def setColor(self, color):
        self.color = color
        self.updateLEDs()

    def flash(self, cycles, speed):
        origColor = self.color
        for n in range(cycles):
            time.sleep(speed)
            self.setColor(origColor)
            time.sleep(speed)
            self.setBrightness(0)
        self.setColor(origColor)

    def pulseWindow(self, delay, cycles):

        cycles = min(100, max(1, cycles))

        # HSV: hue, saturation, value (0-255)
        # normalize RGB values for hsv by dividing by 255
        hue, saturation, colorValue = colorsys.rgb_to_hsv(self.color.r / 255, self.color.g / 255, self.color.b / 255)

        for cycle in range(cycles):
            for colorValue in range(1, 256, 1):
                # print("Going up: ", colorValue)
                newR, newG, newB = colorsys.hsv_to_rgb(hue, saturation, colorValue) 
                # normalize new RGB valies from the HLS conversion and set new color with increased limunance
                newR = newR * 255
                newG = newG * 255
                newB = newB * 255
                
                # set the new color of the window
                adjustedColor = Color(math.trunc(newR), math.trunc(newG), math.trunc(newB))
                self.setColor(adjustedColor)
                time.sleep(delay)
            for colorValue in range(254, 1, -1):
                # print("ColorValue going down: ", colorValue)    
                newR, newG, newB = colorsys.hsv_to_rgb(hue, saturation, colorValue) 
                # normalize new RGB valies from the HLS conversion and set new color with increased limunance
                newR = newR * 255
                newG = newG * 255
                newB = newB * 255
                
                # set the new color of the window
                adjustedColor = Color(math.trunc(newR), math.trunc(newG), math.trunc(newB))
                self.setColor(adjustedColor)
                time.sleep(delay)

class sign:
    def __init__(self, color, brightness):
        self.color = color if color is not None else Color(0.0,0)
        self.brightness = brightness if brightness is not None else 0

#setup some comnstants
LED_COUNT      = 40     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# blue = Color(0,0,255)
# black = Color(0,0,0)
# white = Color(255,255,255)
# red = Color(255,0,0)
# purple = Color(127,0,255)

# Create NeoPixel object with appropriate configuration.
lightStrip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# # Intialize the library (must be called once before other functions).
lightStrip.begin()
