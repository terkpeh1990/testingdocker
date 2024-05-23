from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erpproject.settings')

app = Celery('erpproject',broker='redis://127.0.0.1:6379')
app.conf.enable_utc = False

app.conf.update(timezone = 'Africa/Accra')

app.config_from_object(settings, namespace='CELERY')

#Celery Beat Settings
app.conf.beat_schedule ={
 'send-alert-every-day-at-10:18':{
     'task': 'inventory.tasks.low_stock_alert',
     'schedule': crontab(hour=0, minute=25),
 }
}

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


