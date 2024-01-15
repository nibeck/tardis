from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField

class ControlForm(FlaskForm):
    windowColor = StringField('Color')