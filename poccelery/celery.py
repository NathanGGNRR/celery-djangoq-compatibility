import os
from celery import Celery
from celery.signals import setup_logging


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poccelery.settings")

app = Celery("poccelery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
# app.conf.task_ignore_result = True  # TO COMMENT IF WANT RESULT IN REDIS

@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings

    dictConfig(settings.LOGGING)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
