import os
from . import db

from flask import Flask
from celery import Celery, Task


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis",
            result_backend="redis://redis",
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()

    db.init_app(app)
    celery = celery_init_app(app)
    init_routes(app)

    # from werkzeug.middleware.proxy_fix import ProxyFix
    #
    # app.wsgi_app = ProxyFix(app.wsgi_app)

    return app, celery


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def init_routes(app: Flask):
    from .routes import main
    from .routes.task import task

    app.register_blueprint(main)
    app.register_blueprint(task)
