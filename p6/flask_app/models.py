from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.FileField()
    description = db.StringField()
    verify_code = db.StringField(required=True)
    status = db.BooleanField(required=True) # are you verified?

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Project(db.Document):
    owner = db.ReferenceField(User, required=True)
    title = db.StringField(required=True, min_length=1, max_length=100)
    project_id = db.StringField(required=True)
    description = db.StringField(required=True, min_length=5, max_length=500)

    def get_id(self):
        return self.project_id


class Entry(db.Document):
    project_id = db.StringField(required=True)
    project_title = db.StringField(required=True, min_length=1, max_length=100)
    date = db.StringField(required=True)
    title = db.StringField(required=True, min_length=1, max_length=100)
    content = db.StringField(required=True, min_length=5, max_length=500)


class Comment(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    project_id = db.StringField(required=True, min_length=9, max_length=9)
    project_title = db.StringField(required=True, min_length=1, max_length=100)
