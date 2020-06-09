from wtforms import StringField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Length


class RegisterForm(FlaskForm):
    """Form for registering new user."""

    username = StringField("Username",
                           validators=[InputRequired(),
                           Length(1, 20)])
    password = StringField('Password', validators=[InputRequired()])
    email = StringField('Email Address',
                        validators=[InputRequired(),
                        Length(1, 50)])
    first_name = StringField('First Name',
                        validators=[InputRequired(),
                        Length(1, 30)]) 
    last_name = StringField('Last name',
                        validators=[InputRequired(),
                        Length(1, 30)])


class LoginForm(FlaskForm):
    """Form for logging in user"""

    username = StringField("Username",
                           validators=[InputRequired(),
                           Length(1, 20)])
    password = StringField('Password', validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """Form to add feedback"""

    title = StringField('Title',
                        validators=[InputRequired(), Length(1, 100)])
    content = TextAreaField('Content', validators=[InputRequired()])

