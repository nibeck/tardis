from rpi_ws281x import *

BLUE    = Color(0,0,255)
BLACK   = Color(0,0,0)
WHITE   = Color(255,255,255)
RED     = Color(255,0,0)
PURPLE  = Color(127,0,255)
YELLOW  = Color(255,255,0)
GREEN   = Color(50,205,50)
TEAL    = Color(100,128,128)
NAVY    = Color(0,0,128)

#setup some comnstants
LED_COUNT      = 40         # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
import models

# Create NeoPixel object with appropriate configuration.
lightStrip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Intialize the library (must be called once before other functions).
lightStrip.begin()

r = 0
g = 204
b = 204

for ix in range(40):
    lightStrip.setPixelColor(ix, BLACK)    

lightStrip.show()
