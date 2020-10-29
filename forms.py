from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, NumberRange, URL, AnyOf, Length

class RegisterUserForm(FlaskForm):
    """Form for creating a new user"""
    username = StringField("Username", validators=[Length(max=20, message="Username can not be more than 20 characters"), InputRequired(message="Username is required")])
    password = PasswordField("Password", validators=[InputRequired(message="Password is required")])
    email = StringField("Email", validators=[Email(message="Email must be valid"), InputRequired(message="Email is required")])
    first_name = StringField("First Name", validators=[Length(max=30, message="First name can not be more than 30 characters"), InputRequired(message="First name is required")])
    last_name = StringField("Last Name", validators=[Length(max=30, message="Last name can not be more than 30 characters"), InputRequired(message="Last name is required")])

class LoginUSerForm(FlaskForm):
    """Form for logging-in an existing user"""
    username = StringField("Username", validators=[InputRequired(message="Username is required")])
    password = PasswordField("Password", validators=[InputRequired(message="Password is required")])