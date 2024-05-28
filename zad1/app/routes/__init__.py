from celery.result import AsyncResult
from flask import Blueprint, redirect, render_template, request, url_for
from ..models import add_message, get_messages
from .. import tasks
from ..db import get_db


main = Blueprint("main", __name__)


@main.route("/index")
@main.route("/")
def index():
    return render_template("index.html")


@main.route("/form", methods=["GET", "POST"])
def form():
    errors = {}
    success = False

    if request.method == "POST":
        title = request.form["title"]
        message = request.form["content"]

        if not title:
            errors["title"] = "Title not provided"
        if not message:
            errors["message"] = "Message Content not provided"

        if not errors:
            add_message(title, message)
            success = True

    return render_template("form.html", errors=errors, success=success)


@main.route("/async-form")
def async_form():
    if request.method == "POST":
        tasks.add_message.delay(request.form)
        return redirect(url_for("async_form"))

    return render_template("async_form.html", errors={}, success=False)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/messages")
def messages():
    return render_template("messages.html", messages=get_messages())
