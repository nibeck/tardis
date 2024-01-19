import time
import signal
import sys
import math
from rpi_ws281x import *
from app.models import TARDIS
from flask import request
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import ControlForm

# TODO: Add Top Light to model
# TODO: Validate all inputs
# TODO: Implement bootstrap
# TODO: Invetigate ruuning asyn or in parallel 

BLUE    = Color(0,0,255)
BLACK   = Color(0,0,0)
WHITE   = Color(255,255,255)
RED     = Color(255,0,0)
PURPLE  = Color(127,0,255)
YELLOW  = Color(255,255,0)
GREEN   = Color(50,205,50)
TEAL    = Color(100,128,128)
NAVY    = Color(0,0,128)

# color cobversion function - return RGB of Color() object
def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    # print red, green, blue
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

# Create TARDIS object
myTARDIS = TARDIS("Mike Nibeck", app.config['RED'])
print("The doctor is in", myTARDIS.doctor)

myTARDIS.frontWindow.turnOff()
myTARDIS.backWindow.turnOff()

@app.route('/', methods=('GET', 'POST'))
@app.route('/index')
def index():
    user = {'username':'Mike'}
    # Set values from TARDIOS Object
    form=ControlForm(tardis_doctor = 'Tom Baker',
                     back_window_brightness = myTARDIS.backWindow.brightness,
                     back_window_color = myTARDIS.backWindow.color,
                     front_window_brightness = myTARDIS.frontWindow.brightness,
                     front_window_color = myTARDIS.frontWindow.color,
                     right_window_brightness = myTARDIS.rtWindow.brightness,
                     right_window_color = myTARDIS.rtWindow.color,
                     left_window_brightness = myTARDIS.leftWindow.brightness,
                     left_window_color = myTARDIS.leftWindow.color)
    if form.validate_on_submit():
        return redirect('index.html')
    
    # Update Frontwindow

    selected_color = request.form.get('color-input')

    newColor = getRGBfromI(int(form.front_window_color.data))
    myTARDIS.frontWindow.color = Color(newColor[0], newColor[1], newColor[2])
    myTARDIS.frontWindow.brightness = form.front_window_brightness.data
    if form.front_window_brightness.data == 0:
        myTARDIS.frontWindow.turnOff()
    else :
        myTARDIS.frontWindow.turnOn()

    #Update Rear Window
    newColor = getRGBfromI(int(form.back_window_color.data ))
    myTARDIS.backWindow.color = Color(newColor[0], newColor[1], newColor[2])
    myTARDIS.frontWindow.brightness = form.back_window_brightness.data
    if form.back_window_brightness.data == 0:
        myTARDIS.backWindow.turnOff()
    else :
        myTARDIS.backWindow.turnOn()

    #Update Right Window
    newColor = getRGBfromI(int(form.right_window_color.data ))
    myTARDIS.rtWindow.color = Color(newColor[0], newColor[1], newColor[2])
    myTARDIS.rtWindow.brightness = form.right_window_brightness.data
    if form.right_window_brightness.data == 0:
        myTARDIS.rtWindow.turnOff()
    else :
        myTARDIS.rtWindow.turnOn()
    
    #Update Left Window
    newColor = getRGBfromI(int(form.left_window_color.data ))
    myTARDIS.leftWindow.color = Color(newColor[0], newColor[1], newColor[2])
    myTARDIS.leftWindow.brightness = form.left_window_brightness.data
    if form.left_window_brightness.data == 0:
        myTARDIS.leftWindow.turnOff()
    else :
        myTARDIS.leftWindow.turnOn()
    return render_template('index.html', title='Your Own TARDIS', user=user, form=form)

@app.route('/tardis/off')
def off():
    myTARDIS.turnOff()
    return 'Bye!'  

@app.route('/flashes')
def flashTest():
    myTARDIS.backWindow.color = '255,255,255'
    myTARDIS.backWindow.turnOn()
    myTARDIS.backWindow.pulseWindow(2, .005)
    myTARDIS.backWindow.color = app.config['RED']
    myTARDIS.backWindow.pulseWindow(2, .005)
    myTARDIS.backWindow.color = app.config['YELLOW']
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