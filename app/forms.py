from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, NumberRange

class ControlForm(FlaskForm):
    tardis_color = StringField('TARDIS Color')
    tardis_doctor = StringField('The doctor\'s name')

    front_window_color = StringField('Window Color')
    front_window_state = BooleanField('On/Off', default=True)
    front_window_brightness =  IntegerField('Brightness',validators=[InputRequired(), 
                                                                     NumberRange(0, 100, 'Must be between 0 and 100') ])
    back_window_color = StringField('Window Color')
    back_window_state = BooleanField('On/Off')
    back_window_brightness =  IntegerField('Brightness',validators=[InputRequired(), 
                                                                    NumberRange(0, 100, 'Must be between 0 and 100') ])
    right_window_color = StringField('Window Color')
    right_window_state = BooleanField('On/Off')
    right_window_brightness =  IntegerField('Brightness',validators=[InputRequired(), 
                                                                     NumberRange(0, 100, 'Must be between 0 and 100') ])

    left_window_color = StringField('Window Color')   
    left_window_state = BooleanField('On/Off', default=True)    
    left_window_brightness =  IntegerField('Brightness',
                                           validators=[InputRequired(), 
                                                        NumberRange(0, 100, 'Must be between 0 and 100') ])

    submit = SubmitField('Update')
