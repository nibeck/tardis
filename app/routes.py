import time
import signal
import sys
import math
import json

from rpi_ws281x import *
from app.models import TARDIS
from flask import request
from flask import render_template, flash, redirect, url_for, jsonify
from app import app
from app.forms import ControlForm
from app.color_util import getRGBfromI, getIfromRGB, rgb_to_hex, hex_to_rgb
from pprint import pprint

# TODO: Add Top Light to model
# TODO: Invetigate ruuning asyn or in parallel

BLUE = Color(0, 0, 255)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
PURPLE = Color(127, 0, 255)
YELLOW = Color(255, 255, 0)
GREEN = Color(50, 205, 50)
TEAL = Color(100, 128, 128)
NAVY = Color(0, 0, 128)


# # color cobversion function - return RGB of Color() object
# def getRGBfromI(RGBint):
#     blue = RGBint & 255
#     green = (RGBint >> 8) & 255
#     red = (RGBint >> 16) & 255
#     return red, green, blue


# def getIfromRGB(rgb):
#     red = rgb[0]
#     green = rgb[1]
#     blue = rgb[2]
#     # print red, green, blue
#     RGBint = (red << 16) + (green << 8) + blue
#     return RGBint


# def rgb_to_hex(r, g, b):
#     return "#{:02x}{:02x}{:02x}".format(r, g, b)


# def hex_to_rgb(hex):
#     rgb = []
#     for i in (0, 2, 4):
#         decimal = int(hex[i : i + 2], 16)
#         rgb.append(decimal)

#     return tuple(rgb)

# Create TARDIS object
myTARDIS = TARDIS("Mike Nibeck", app.config["RED"])

pprint(vars(myTARDIS), indent=2)
pprint(vars(myTARDIS.frontWindow))


@app.route("/", methods=("GET", "POST"))
@app.route("/index")
def index():
    # Set values from TARDIS Object

    form = ControlForm(
        tardis_doctor=myTARDIS.doctor,
        back_window_brightness=myTARDIS.backWindow.brightness,
        back_window_color=myTARDIS.backWindow.color,
        front_window_brightness=myTARDIS.frontWindow.brightness,
        front_window_color=myTARDIS.frontWindow.color,
        right_window_brightness=myTARDIS.rtWindow.brightness,
        right_window_color=myTARDIS.rtWindow.color,
        left_window_brightness=myTARDIS.leftWindow.brightness,
        left_window_color=myTARDIS.leftWindow.color,
    )

    if form.validate_on_submit():
        return redirect("index.html")

    # Update Rear Window
    newColor = getRGBfromI(int(form.back_window_color.data))
    myTARDIS.backWindow.color = Color(newColor[0], newColor[1], newColor[2])
    myTARDIS.frontWindow.brightness = form.back_window_brightness.data
    if form.back_window_brightness.data == 0:
        myTARDIS.backWindow.turnOff()
    else:
        myTARDIS.backWindow.turnOn()

    return render_template("index.html", title="Your Own TARDIS", form=form)


@app.route("/tardis/off")
def off():
    form = ControlForm(
        tardis_doctor=myTARDIS.doctor,
        back_window_brightness=myTARDIS.backWindow.brightness,
        back_window_color=myTARDIS.backWindow.color,
        front_window_brightness=myTARDIS.frontWindow.brightness,
        front_window_color=myTARDIS.frontWindow.color,
        right_window_brightness=myTARDIS.rtWindow.brightness,
        right_window_color=myTARDIS.rtWindow.color,
        left_window_brightness=myTARDIS.leftWindow.brightness,
        left_window_color=myTARDIS.leftWindow.color,
    )
    myTARDIS.turnOff()
    return render_template("index.html", title="Your Own TARDIS", form=form)


@app.route("/flashes")
def flashTest():
    myTARDIS.backWindow.color = Color(255, 255, 255)
    myTARDIS.backWindow.turnOn()
    myTARDIS.backWindow.pulseWindow(2, 0.005)
    myTARDIS.backWindow.color = app.config["RED"]
    myTARDIS.backWindow.pulseWindow(2, 0.005)
    myTARDIS.backWindow.color = app.config["YELLOW"]
    myTARDIS.backWindow.pulseWindow(2, 0.005)
    myTARDIS.backWindow.flash(5, 0.1)
    time.sleep(1)

    myTARDIS.turnOff()
    return render_template("index.html", title="Your Own TARDIS", form=form)


@app.route("/window/front/pulse", methods=["GET", "POST"])
def front_window_pulseWindow():
    form = ControlForm(
        tardis_doctor=myTARDIS.doctor,
        back_window_brightness=myTARDIS.backWindow.brightness,
        back_window_color=myTARDIS.backWindow.color,
        front_window_brightness=myTARDIS.frontWindow.brightness,
        front_window_color=myTARDIS.frontWindow.color,
        right_window_brightness=myTARDIS.rtWindow.brightness,
        right_window_color=myTARDIS.rtWindow.color,
        left_window_brightness=myTARDIS.leftWindow.brightness,
        left_window_color=myTARDIS.leftWindow.color,
    )
    cycles = request.args.get("cycles")
    delay = request.args.get("delay")
    print("Cycles:", cycles, " Delay=", delay)
    myTARDIS.frontWindow.pulseWindow(int(cycles), float(delay))

    return render_template("index.html", title="Your Own TARDIS", form=form)


@app.route("/window/front/update_color", methods=["POST"])
def front_window_color():
    print("Updating color")

    form = ControlForm(
        tardis_doctor=myTARDIS.doctor,
        back_window_brightness=myTARDIS.backWindow.brightness,
        back_window_color=myTARDIS.backWindow.color,
        front_window_brightness=myTARDIS.frontWindow.brightness,
        front_window_color=myTARDIS.frontWindow.color,
        right_window_brightness=myTARDIS.rtWindow.brightness,
        right_window_color=myTARDIS.rtWindow.color,
        left_window_brightness=myTARDIS.leftWindow.brightness,
        left_window_color=myTARDIS.leftWindow.color,
    )

    picked_color = request.form.get("color")
    # Strip # from front of hex value
    h = picked_color.lstrip("#")
    # extract RGB values from the hex number.
    rgb = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))

    myTARDIS.frontWindow.color = Color(rgb[0], rgb[1], rgb[2])
    form.front_window_color = Color(rgb[0], rgb[1], rgb[2])

    myTARDIS.frontWindow.turnOn()
    return render_template("index.html", title="Your Own TARDIS", form=form)


@app.route("/window/update_color", methods=["POST"])
def update_window_color():
    print("window/update_color/ Updating color from web form")

    form = ControlForm(
        tardis_doctor=myTARDIS.doctor,
        back_window_brightness=myTARDIS.backWindow.brightness,
        back_window_color=myTARDIS.backWindow.color,
        front_window_brightness=myTARDIS.frontWindow.brightness,
        front_window_color=myTARDIS.frontWindow.color,
        right_window_brightness=myTARDIS.rtWindow.brightness,
        right_window_color=myTARDIS.rtWindow.color,
        left_window_brightness=myTARDIS.leftWindow.brightness,
        left_window_color=myTARDIS.leftWindow.color,
    )

    what_color = request.values.get("color")
    which_window = request.values.get("window")

    print("Window:", which_window)
    print("Color:", what_color)
    # Strip # from front of hex value
    what_color = what_color.lstrip("#")
    what_color = what_color.lstrip("%")
    print("Color:", what_color)

    rgb = hex_to_rgb(what_color)

    match which_window:
        case "front":
            print("New Front color")
            myTARDIS.frontWindow.color = Color(rgb[0], rgb[1], rgb[2])
            form.front_window_color = Color(rgb[0], rgb[1], rgb[2])
            myTARDIS.frontWindow.turnOn()
        case "rear":
            print("Rear Color")
            myTARDIS.backWindow.color = Color(rgb[0], rgb[1], rgb[2])
            form.back_window_color = Color(rgb[0], rgb[1], rgb[2])
            myTARDIS.rearWindow.turnOn()
        case "right":
            print("Right Color")
            myTARDIS.rtWindow.color = Color(rgb[0], rgb[1], rgb[2])
            form.right_window_color = Color(rgb[0], rgb[1], rgb[2])
            myTARDIS.rtWindow.turnOn()
        case "left":
            print("Left Color")
            myTARDIS.leftWindow.color = Color(rgb[0], rgb[1], rgb[2])
            form.left_window_color = Color(rgb[0], rgb[1], rgb[2])
            myTARDIS.leftWindow.turnOn()

    return render_template("index.html", title="Your Own TARDIS", form=form)


@app.route("/window/front/on", methods=["POST"])
def front_window_on():
    myTARDIS.frontWindow.turnOn()
    print("Turning on")
    return render_template("index.html")


@app.route("/window/front/off", methods=["POST"])
def front_window_off():
    print("Turning off")
    myTARDIS.frontWindow.turnOff()


@app.route("/window/front/update_brightness", methods=["POST"])
def front_window_brightness():
    form = ControlForm(
        tardis_doctor=myTARDIS.doctor,
        back_window_brightness=myTARDIS.backWindow.brightness,
        back_window_color=myTARDIS.backWindow.color,
        front_window_brightness=myTARDIS.frontWindow.brightness,
        front_window_color=myTARDIS.frontWindow.color,
        right_window_brightness=myTARDIS.rtWindow.brightness,
        right_window_color=myTARDIS.rtWindow.color,
        left_window_brightness=myTARDIS.leftWindow.brightness,
        left_window_color=myTARDIS.leftWindow.color,
    )
    picked_brightness = request.form.get("selectedBrightness")
    print("New brightness:", picked_brightness)

    # Set window brightness
    myTARDIS.frontWindow.brightness = int(picked_brightness)
    form.front_window_brightness = myTARDIS.frontWindow.brightness
    if picked_brightness == "0":
        myTARDIS.frontWindow.turnOff()
    else:
        myTARDIS.frontWindow.turnOn()
    return render_template("index.html", title="Your Own TARDIS", form=form)


# main driver function
if __name__ == "__main__":
    #     run() method of Flask class runs the application
    #     on the local development server.
    app.run()


# on ctrl-c, turn LEDs off
def signal_handler(signal, frame):
    myTARDIS.turnOff()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    globals()[sys.argv[1]]()
