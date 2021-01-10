from celery import Celery

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")

celery_app = Celery('celery_tasks')


celery_app.config_from_object('celery_tasks.config')

celery_app.autodiscover_tasks(['celery_tasks.sms'])