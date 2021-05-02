# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

#Talisman
from flask_talisman import Talisman

#Flask_Mail
from flask_mail import Mail

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

from flask_app.users.routes import users
from flask_app.diaries.routes import diaries


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    csp = {
        'default-src': '\'self\'',
        'img-src': '*',
        'style-src': '*'
        }

    Talisman(app, content_security_policy=csp)

    # flask mail configs
    app.config.update(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 465,
        MAIL_USE_SSL = True,
        MAIL_DEFAULT_SENDER = 'projectdiary388j@gmail.com',
        MAIL_USERNAME = 'projectdiary388j@gmail.com',
        MAIL_PASSWORD = 'tasbcbuxdwulngpp'
    )

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(diaries)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
