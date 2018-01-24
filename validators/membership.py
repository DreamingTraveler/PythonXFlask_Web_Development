from flask import request
from wtforms import Form, StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf, Regexp, InputRequired

class RegisterValidator():
    class RegisterForm(Form):
        username = StringField('username', validators=[DataRequired(), Length(6, 20)])#StringField(label, validators)
        password = StringField('password', validators=[DataRequired(), Length(6, 50)])
        realname = StringField('realname', validators=[DataRequired(), Length(1, 50)])
        confirm_password = StringField('confirm_password', validators=[DataRequired(), Length(6, 50), EqualTo('password')])
        email = StringField('email', validators=[DataRequired(), Length(1, 256), Email()])
        sex = StringField('sex', validators=[DataRequired(), AnyOf(['male', 'female', 'others'])])
        birthday = DateField('birthday', validators=[DataRequired()], format='%Y-%m-%d')
        phone = StringField('phone', validators=[DataRequired(), Length(1, 15), Regexp(r'^[\d\-]+$')])
    def validate(self):
        validator = RegisterValidator.RegisterForm(request.form)
        return validator.validate()

class LoginValidator():
    class LoginForm(Form):
        username = StringField('username', validators=[DataRequired(), Length(6, 20)])
        password = StringField('password', validators=[DataRequired(), Length(6, 50)])
    def validate(self):
        validator = LoginValidator.LoginForm(request.form)
        return validator.validate()

class ProfileValidator():
    class ProfileForm(Form):
        old_password = StringField('old_password', validators=[DataRequired(), Length(6, 50)])
        new_password = StringField('new_password', validators=[InputRequired(), Length(6, 50)])
        confirm_new_password = StringField('confirm_new_password', validators=[InputRequired(), Length(6, 50), EqualTo('new_password')])
        realname = StringField('realname', validators=[DataRequired(), Length(1, 50)])
        email = StringField('email', validators=[DataRequired(), Length(1, 256), Email()])
        sex = StringField('sex', validators=[DataRequired(), AnyOf(['male', 'female', 'others'])])
        birthday = DateField('birthday', validators=[DataRequired()], format='%Y-%m-%d')
        phone = StringField('phone', validators=[DataRequired(), Length(1, 15), Regexp(r'^[\d\-]+$')])
    def validate(self):
        validator = ProfileValidator.ProfileForm(request.form)
        return True