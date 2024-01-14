import time
import math
import signal
import sys
from rpi_ws281x import *
import argparse, colorsys
from app.models import TARDIS
from flask import Flask
from flask import request
from flask import render_template
from app import app

# TODO: Invetigate ruuning asyn or in parallel 
# TODO: Wrap in a simple Web UI

BLUE    = Color(0,0,255)
BLACK   = Color(0,0,0)
WHITE   = Color(255,255,255)
RED     = Color(255,0,0)
PURPLE  = Color(127,0,255)
YELLOW  = Color(255,255,0)
GREEN   = Color(50,205,50)
TEAL    = Color(100,128,128)
NAVY    = Color(0,0,128)

# app = Flask(__name__)

# Create TARDIS object
myTARDIS = TARDIS("Mike Nibeck", BLUE)
print("Thge doctor is in", myTARDIS.doctor)

@app.route('/')
@app.route('/index')
def index():
    user = {'usrename':'Mike'}
    print("in the main index route")
    return render_template('index.html', title='Your Own TARDIS', user=user)

@app.route('/tardis/off')
def off():
    myTARDIS.turnOff()
    return 'Bye!'  

@app.route('/flashes')
def flashTest():
    myTARDIS.backWindow.color = BLUE
    myTARDIS.backWindow.turnOn()
    myTARDIS.backWindow.pulseWindow(2, .005)
    myTARDIS.backWindow.color = RED
    myTARDIS.backWindow.pulseWindow(2, .005)
    myTARDIS.backWindow.color = YELLOW
    myTARDIS.backWindow.pulseWindow(2, .005)
    myTARDIS.backWindow.flash(5, .1)
    time.sleep(1)

    myTARDIS.turnOff()
    return'Flashy lights!'

@app.route('/window/front/pulse', methods=['GET', 'POST'])
def front_window_pulseWindow():
    cycles = request.args.get('cycles')
    delay = request.args.get('delay')
    print("Cycles:", cycles, " Delay=", delay)
    myTARDIS.frontWindow.pulseWindow(int(cycles), float(delay))    
    return 'Flashy'

@app.route('/window/front/color', methods=['GET', 'POST'])
def front_window_color():
    color = request.args.get('color')
    print("color arg: ", color)
    myTARDIS.frontWindow.color = color    
    myTARDIS.frontWindow.turnOn()
    return 'Window On'

# main driver function
if __name__ == '__main__': 
#     run() method of Flask class runs the application 
#     on the local development server.
    app.run()

# on ctrl-c, turn LEDs off
def signal_handler(signal, frame):
    myTARDIS.turnOff()  
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    globals()[sys.argv[1]]()