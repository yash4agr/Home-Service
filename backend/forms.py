from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FileField, FloatField, FieldList, IntegerField, DateTimeField, FormField
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

class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    base_price = FloatField('Base Price', validators=[DataRequired(), NumberRange(min=0)])
    time_required = FloatField('Time Required', validators=[DataRequired(), NumberRange(min=0.5)])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    new_category = StringField('New Category', validators=[Optional()])
    tags = FieldList(StringField('Tag'))
    img = FileField('Image', validators=[Optional()])


class BookingRequestForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    
    locality = StringField('Locality', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    
    service_date = DateTimeField('Service Date', validators=[DataRequired()], format='%Y-%m-%d')
    service_time = StringField('Service Time', validators=[DataRequired()])
    payment_method = StringField('Payment Method', validators=[Optional()])
    
    total_amount = FloatField('Total Amount', validators=[DataRequired()])
