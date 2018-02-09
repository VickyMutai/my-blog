from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from ..models import User
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    email = StringField('Enter your Email',validators=[Required(),Email()])
    name = StringField('Full Name: ',validators=[Required()])
    username = StringField('User Name: ',validators=[Required()])
    password = PasswordField('Password', validators=[Required(),
    EqualTo('password_confirm',message='Passwords must match')])
    password_confirm = PasswordField('Confirm Password',validators=[Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError('There is an account with that email')
    def validate_username(self,data_field):
        if User.query.filter_by(username=data_field.data).first():
            raise ValidationError('That username is taken')

class LoginForm(FlaskForm):
    email = StringField('Enter your Email',validators=[Required(),Email()])
    password = PasswordField('Password',validators=[Required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')