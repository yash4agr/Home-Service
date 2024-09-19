from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField,DateTimeField, DateField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional, EqualTo
from datetime import datetime

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])

class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    username = StringField('Display Name', validators=[Length(max=15), DataRequired()])
    dob = DateField('Birthdate', format='%Y-%m-%d', validators=[Optional()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    img = FileField('Image File', 
                    default=None,  
                    validators=[Optional(), FileAllowed(['jpg', 'jpeg'], 'Only JPEG images are allowed.')]
                    )
