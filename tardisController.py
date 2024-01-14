#include all necessary packages to get LEDs to work with Raspberry Pi
import time
import math
import signal
import sys
from rpi_ws281x import *
import argparse
import colorsys
from tardis import TARDIS

from flask import Flask

BLUE    = Color(0,0,255)
BLACK   = Color(0,0,0)
WHITE   = Color(255,255,255)
RED     = Color(255,0,0)
PURPLE  = Color(127,0,255)
YELLOW  = Color(255,255,0)
GREEN   = Color(50,205,50)
TEAL    = Color(100,128,128)
NAVY    = Color(0,0,128)

# TODO: Invetigate ruuning asyn or in parallel 
# TODO: Wrap in a simple Web UI

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello TARDIS !!!!'

# main driver function
# if __name__ == '__main__':
 
#     run() method of Flask class runs the application 
#     on the local development server.
#     app.run()

# on ctrl-c, turn LEDs off
def signal_handler(signal, frame):
    myTARDIS.turnOff()  
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

myTARDIS = TARDIS("Mike Nibeck", BLUE)
print("After TARDIS create")
myTARDIS.backWindow.color = BLUE
myTARDIS.backWindow.turnOn()
myTARDIS.backWindow.pulseWindow(2, .005)
myTARDIS.backWindow.color = RED
myTARDIS.backWindow.pulseWindow(2, .005)
myTARDIS.backWindow.color = PURPLE
myTARDIS.backWindow.pulseWindow(2, .005)
myTARDIS.backWindow.color = YELLOW
myTARDIS.backWindow.pulseWindow(2, .005)
myTARDIS.backWindow.flash(5, .1)

time.sleep(1)
myTARDIS.turnOff()