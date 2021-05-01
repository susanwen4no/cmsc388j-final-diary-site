from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import CreateDiaryForm, EntryForm, DiaryCommentForm
from ..models import User

from . import diaries

@diaries.route("/")
def index():


    return render_template("index.html")


@diaries.route("/create-project")
@login_required
def create_project():
    return "create project"
''''
    form = CreateDiaryForm()

    render_template("create_project.html", form=form)
'''

@diaries.route("/user/<username>")
def user_detail(username):
    return "nope"
    #render_template("user_detail.html")


@diaries.route("/projects/<project_id>")
def project(project_id):

    comment_form = DiaryCommentForm()

    if comment_form.submit.data and comment_form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            commenter=current_user._get_current_object(),
            content=comment_form.content.data,
            date=current_time(),
            project_id=project_id,
            project_title=result.title,
        )
        comment.save()

        return redirect(request.path)

    entry_form = EntryForm()

    if entry_form.submit_en.data and entry_form.validate_on_submit() and current_user.is_authenticated:
        entry = Entry(
            content=entry_form.content.data,
            title=entry_form.title.data,
            date=current_time(),
            project_id=project_id,
            project_title=result.title,
        )
        entry.save()
        return redirect(request.path)

    project = Project.object(project_id=project_id)
    comments = Comment.object(project_id=project_id)
    entries = Entry.object(project_id=project_id)

    render_template(
        "project_detail.html", comment_form=comment_form, entry_form=entry_form,
        comments=comments, entries=entries, project=project
        )

