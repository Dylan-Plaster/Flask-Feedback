from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Optional, Email, NumberRange, URL, AnyOf, Length

class RegisterUserForm(FlaskForm):
    """Form for creating a new user"""
    username = StringField("Username", validators=[Length(max=20, message="Username can not be more than 20 characters"), InputRequired(message="Username is required")])
    password = PasswordField("Password", validators=[InputRequired(message="Password is required")])
    email = StringField("Email", validators=[Email(message="Email must be valid"), InputRequired(message="Email is required")])
    first_name = StringField("First Name", validators=[Length(max=30, message="First name can not be more than 30 characters"), InputRequired(message="First name is required")])
    last_name = StringField("Last Name", validators=[Length(max=30, message="Last name can not be more than 30 characters"), InputRequired(message="Last name is required")])

class LoginUserForm(FlaskForm):
    """Form for logging-in an existing user"""
    username = StringField("Username", validators=[InputRequired(message="Username is required")])
    password = PasswordField("Password", validators=[InputRequired(message="Password is required")])

class FeedbackForm(FlaskForm):
    """Form for creating/updating feedback posts"""
    title = StringField("Title", validators=[Length(max=100, message="Title can not be more than 100 characters"), InputRequired(message="Title is required")])
    content = TextAreaField("Content", validators=[InputRequired(message="Content is required")])