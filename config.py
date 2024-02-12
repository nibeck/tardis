import os
from rpi_ws281x import *

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
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
