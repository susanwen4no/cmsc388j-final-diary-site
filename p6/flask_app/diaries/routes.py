from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from ..utils import current_time

from .. import bcrypt
from ..forms import CreateDiaryForm, EntryForm, DiaryCommentForm
from ..models import User, Comment, Entry, Project

from . import diaries

@diaries.route("/")
def index():
    #TODO
    return render_template("index.html")


@diaries.route("/user/<username>")
def user_detail(username):
    #TODO
    return "nope"
    #render_template("user_detail.html")


@diaries.route("/create", methods=["GET", "POST"])
@login_required
def create():
    
    form = CreateDiaryForm()

    if form.validate_on_submit():
        pid = current_time().strip()+current_user.username 
        #project id is time of creation + username
        proj = Project(
            owner=current_user._get_current_object(),
            title=form.title.data,
            project_id=pid,
            description=form.description.data,
        )
        
        proj.save()
        flash("Project created!")
        return redirect(url_for("diaries.project", project_id=pid))

    return render_template("create_project.html", form=form)


@diaries.route("/project/<project_id>", methods=["GET", "POST"])
def project(project_id):
    
    comment_form = DiaryCommentForm()
    project = Project.objects(project_id=project_id).first()

    if comment_form.submit.data and comment_form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            commenter=current_user._get_current_object(),
            content=comment_form.text.data,
            date=current_time(),
            project_id=project_id,
            project_title=project.title,
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
            project_title=project.title,
        )
        entry.save()
        return redirect(request.path)

    comments = Comment.objects(project_id=project_id)
    entries = Entry.objects(project_id=project_id)

    return render_template(
        "project_detail.html", comment_form=comment_form, entry_form=entry_form,
        comments=comments, entries=entries, project=project, username=project.owner.username
        )
    

