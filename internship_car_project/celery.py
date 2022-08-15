import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internship_car_project.settings')
celery_app = Celery('internship_car_project')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "add-cars-every-three-minutes": {
        "task": "src.car.tasks.car_task",
        "schedule": crontab(minute="*/3"),
    },
    "buy-showroom-dealer-every-single-minute": {
        "task": "src.showroom.tasks.showroom_task",
        "schedule": crontab(minute="*/1"),
    },
    "buy-customer-showroom-every-two-minutes": {
        "task": "src.customer.tasks.customer_task",
        "schedule": crontab(minute="*/2"),
    },
}
