import os
from celery import Celery
from django.conf import settings
import celery.signals


@celery.signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "userMangment.settings")
app = Celery('userMangment')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
