import time
from celery.result import AsyncResult
from flask import Blueprint, jsonify, request


task = Blueprint("task", __name__, url_prefix="/task")


@task.route(("/messages"))
def messages():
    from ..tasks import get_messages

    task = get_messages.delay()
    return task.id


@task.post(("/form"))
def form():
    from .. import tasks

    form_data = {key: value for key, value in request.form.items()}
    task = tasks.add_message.delay(form_data)
    return jsonify({"task_id": task.id})


@task.route("/check/<string:task_id>")
def result(task_id):
    res = AsyncResult(task_id)
    return jsonify({"status": res.status, "result": res.result})
