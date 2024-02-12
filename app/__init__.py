from flask import Flask
from config import Config
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object(Config)

# toolbar = DebugToolbarExtension(app)

from app import routes, models
