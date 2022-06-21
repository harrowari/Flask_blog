from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, InputRequired, Regexp
from blog.models import User



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()]) 
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Registration form and validation adapted from Grinberg, 2017

class RegistrationForm(FlaskForm):
    username = StringField('First Name', validators=[InputRequired(), Regexp('^[a-zA-Z0-9]{4,20}$',)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Regexp('^[a-zA-Z0-9]{4,20}$',)])
    password2 = PasswordField(
        'Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CommentForm(FlaskForm):
    body = StringField('Body')
    submit = SubmitField('Submit')

class SortPosts(FlaskForm):
    order = SelectField(label="Sort by date", choices=[('date_desc', 'Descending'), ('date_asc', 'Ascending')], render_kw={"onchange": "submit();"})


