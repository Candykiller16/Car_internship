from celery import shared_task

from src.car.management.commands.add_cars import add_cars_for_dealer


@shared_task
def car_task():
    add_cars_for_dealer()
