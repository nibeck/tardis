from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
)


class ControlForm(FlaskForm):
    tardis_light_color = StringField("TARDIS Light Color")
    submit = SubmitField("Update")
