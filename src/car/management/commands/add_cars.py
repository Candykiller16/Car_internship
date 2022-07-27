import random

from django.core.management.base import BaseCommand

from src.dealer.models import Dealer
from src.car.models import Car
from src.showroom.models import Showroom
from src.customer.models import Customer
from core.data_and_funcs import cars_models, get_random_color, get_random_year, \
    get_random_transmission, get_random_body_type, districts, customer_list


def add_cars_for_dealer():
    for key in list(cars_models.keys()):
        for j in range(3):
            car_for_dealer = Car.objects.create(name=key,
                                                model=f"Model {random.choice(list(cars_models[key]))}",
                                                body_type=get_random_body_type(),
                                                transmission_type=get_random_transmission(),
                                                color=get_random_color(),
                                                year=get_random_year(),
                                                price=random.randint(5000, 15000),
                                                dealer=Dealer.objects.get(name=f"{key} Dealer"))


def add_cars_for_everybody():
    for key in list(cars_models.keys()):
        for j in range(3):
            car_for_everybody = Car.objects.create(name=key,
                                                   model=f"Model {random.choice(list(cars_models[key]))}",
                                                   body_type=get_random_body_type(),
                                                   transmission_type=get_random_transmission(),
                                                   color=get_random_color(),
                                                   year=get_random_year(),
                                                   price=random.randint(5000, 15000),
                                                   dealer=Dealer.objects.get(name=f"{key} Dealer"),
                                                   showroom=Showroom.objects.get(
                                                       name=f"{random.choice(districts)} Showroom"),
                                                   customer=Customer.objects.get(
                                                       name=f"{random.choice(customer_list)}"))

    print('Added cars for everybody')


class Command(BaseCommand):
    help = u'Add cars for everybody'

    def handle(self, *args, **options):
        # add_cars_for_everybody()
        add_cars_for_dealer()
        return 'Done'
