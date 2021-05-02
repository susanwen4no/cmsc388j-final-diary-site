from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

import re

from .models import User

### User Management Forms

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email(),])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

    def validate_password(self, password):
        regex = ("^(?=.*\\d)" +
             "(?=.*[-+_!@#$%^&*., ?]).+$")

        p = re.compile(regex)

        if (not re.search(p, password.data)):
            raise ValidationError("Please use at least 1 number and 1 special character")


class ConfirmationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    code = StringField("Confirmation Code", validators=[InputRequired()])
    submit = SubmitField("Confirm")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class UpdateProfilePicForm(FlaskForm):
    picture = FileField(validators=[InputRequired(), FileAllowed(['jpg', 'png'], 'Images Only!')])
    submit_pp = SubmitField("Update")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")


class UpdateDescriptionForm(FlaskForm):
    description = TextAreaField("Description", validators=[InputRequired()])
    submit_desc = SubmitField("Update Description")

### Other Functionality Form

class CreateDiaryForm(FlaskForm):
    title = StringField(
        "Project Title", validators=[InputRequired(), Length(min=1, max=100)]
    )
    description = TextAreaField(
        "Description", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Create Diary")

class EntryForm(FlaskForm):
    title = StringField(
        "Entry Title", validators=[InputRequired(), Length(min=1, max=100)]
    )
    content = TextAreaField(
        "Description", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit_en = SubmitField("Write Entry")

class DiaryCommentForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")
