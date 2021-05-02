from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from ..utils import current_time

from .. import bcrypt, mail
from werkzeug.utils import secure_filename

from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, ConfirmationForm, UpdateDescriptionForm, UpdateProfilePicForm
from ..models import User

from . import users

# images
import io
import base64

# Flask_Mail
from flask_mail import Message

@users.route("/about")
def about():
    return render_template('about.html')

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("diaries.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        code = "confirmation123"

        user = User(
            username=form.username.data, email=form.email.data, password=hashed, status=False,
            verify_code=code
        )
        user.save()

        # Send confirmation code email!!!
        msg = Message(
            subject="Project Diary Confirmation Code",
            body="Hello! Your confirmation code is: "+code,
            recipients=[user.email]
        )
        mail.send(msg)

        return redirect(url_for("users.verify"))

    return render_template("register.html", title="Register", form=form)


@users.route("/verify", methods=["GET", "POST"])
def verify():
    if current_user.is_authenticated:
        return redirect(url_for("diaries.index"))

    form = ConfirmationForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ) and form.code.data == user.verify_code:

            user.modify(status=True)
            return redirect(url_for("users.login"))

        else:
            flash("Confirmation failed. Try again.")
            return redirect(url_for("users.verify"))

    return render_template("verify.html", title="Verify Account", form=form)
    

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("diaries.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None:
            if user.status and bcrypt.check_password_hash(
                user.password, form.password.data
            ):
                login_user(user)
                return redirect(url_for("users.account"))
            elif not user.status:
                flash("Please verify your account first.")
                return redirect(url_for("users.verify")) 
        else:
            flash("Login failed.")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("diaries.index"))


def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username_form = UpdateUsernameForm()
    description_form = UpdateDescriptionForm()
    pic_form = UpdateProfilePicForm()

    if username_form.validate_on_submit():
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for("users.account"))
    
    if description_form.submit_desc.data and description_form.validate_on_submit():
        current_user.modify(description=description_form.description.data)
        current_user.save()
        return redirect(url_for("users.account"))

    if pic_form.submit_pp.data and pic_form.validate_on_submit():
        img = pic_form.picture.data
        filename = secure_filename(img.filename)
        content_type = f'images/{filename[-3:]}'

        if current_user.profile_pic.get() is None:
            current_user.profile_pic.put(img.stream, content_type=content_type)
        else:
            current_user.profile_pic.replace(img.stream, content_type=content_type)
        
        current_user.save()
        return redirect(url_for("users.account"))

    return render_template(
        "account.html",
        title="Account",
        username_form=username_form,
        description_form=description_form,
        picture_form=pic_form,
        image=get_b64_img(current_user.username)
    )
