import os

from celery import Celery, platforms

from tasks import celery_conf


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")
platforms.C_FORCE_ROOT = True
celery_app = Celery('swiper')
celery_app.config_from_object(celery_conf)
celery_app.autodiscover_tasks()
