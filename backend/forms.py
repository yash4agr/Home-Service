from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField,DateTimeField, DateField, FileField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional, EqualTo, NumberRange
from datetime import datetime

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    username = StringField('Display Name', validators=[Length(max=15), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    # img = FileField('Image File', 
    #                 default=None,  
    #                 validators=[Optional(), FileAllowed(['jpg', 'jpeg'], 'Only JPEG images are allowed.')]
    #                 )

class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = StringField('Description', validators=[DataRequired()])
    base_price = FloatField('Base Price', validators=[DataRequired(), NumberRange(min=0)])
    img = StringField('Image URL', validators=[Length(max=255)])
    time_required = IntegerField('Time Required', validators=[DataRequired(), NumberRange(min=1)])
    available = StringField('Available', validators=[DataRequired()])