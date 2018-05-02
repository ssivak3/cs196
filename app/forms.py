from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
class SignUpForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('sign up')
class createScore(FlaskForm):
    title = StringField('enter title', validators=[DataRequired()])
    composer = StringField('composer name')
    #lyricist = StringField('lyricist')
    #copyright = StringField('copyright')
    timesignature = StringField('top number', 'bottom number')
    keysignature = StringField('')
    submit = SubmitField('get started')
