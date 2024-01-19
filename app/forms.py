from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, BooleanField, SubmitField, RadioField, SelectField

from wtforms.validators import InputRequired, Length, NumberRange

class ControlForm(FlaskForm):
    tardis_color = StringField('TARDIS Color')
    tardis_doctor = StringField('The doctor\'s name')
    front_window_color = SelectField('Window Color', choices=[('16777215', 'White'), 
                                                              ('0', 'Black'),
                                                              ('16711680', 'Red'),
                                                              ('8323327', 'Purple'),
                                                              ('16776960', 'Yellow'),
                                                              ('3329330', 'Green'),
                                                              ('255', 'Blue')
                                                              ])
    front_window_state = BooleanField('On/Off')
    front_window_brightness = IntegerField('Brightness',
                                           validators=[InputRequired(), 
                                                        NumberRange(min=0, max=100, message='Must be between 0 and 100') ])
    back_window_color = SelectField('Window Color', choices=[('16777215', 'White'), 
                                                              ('0', 'Black'),
                                                              ('16711680', 'Red'),
                                                              ('8323327', 'Purple'),
                                                              ('16776960', 'Yellow'),
                                                              ('3329330', 'Green'),
                                                              ('255', 'Blue')
                                                              ])
    back_window_state = BooleanField('On/Off')
    back_window_brightness =  IntegerField('Brightness',
                                           validators=[InputRequired(), 
                                                        NumberRange(min=0, max=100, message='Must be between 0 and 100') ])
    right_window_color = SelectField('Window Color', choices=[('16777215', 'White'), 
                                                              ('0', 'Black'),
                                                              ('16711680', 'Red'),
                                                              ('8323327', 'Purple'),
                                                              ('16776960', 'Yellow'),
                                                              ('3329330', 'Green'),
                                                              ('255', 'Blue')
                                                              ])
    right_window_state = BooleanField('On/Off')
    right_window_brightness =  IntegerField('Brightness',
                                            validators=[InputRequired(), 
                                                        NumberRange(min=0, max=100, message='Must be between 0 and 100') ])

    left_window_color = SelectField('Window Color', choices=[('16777215', 'White'), 
                                                              ('0', 'Black'),
                                                              ('16711680', 'Red'),
                                                              ('8323327', 'Purple'),
                                                              ('16776960', 'Yellow'),
                                                              ('3329330', 'Green'),
                                                              ('255', 'Blue')
                                                              ])   
    left_window_state = BooleanField('On/Off')    
    left_window_brightness =  IntegerField('Brightness',
                                           validators=[InputRequired(), 
                                                        NumberRange(min=0, max=100, message='Must be between 0 and 100') ])

    submit = SubmitField('Update')
