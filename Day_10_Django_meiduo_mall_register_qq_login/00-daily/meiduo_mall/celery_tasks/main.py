from celery import Celery

app = Celery('meiduo')

app.config_from_object('celery_tasks.config')

app.autodiscover_tasks(['celery_tasks.main'])
