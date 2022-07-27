from django.core.management.base import BaseCommand

from src.users.models import CustomUser
from core.data_and_funcs import cars_models


def add_dealers():
    for key in list(cars_models):
        dealers = CustomUser.objects.create_user(username=f'{key}_dealer',
                                                 first_name=f'{key} Dealer',
                                                 email=f'{key}@mail.ru', password='123',
                                                 is_superuser=False,
                                                 is_staff=False, is_dealer=True)

    print('Added dealers')


# def add_cars_for_dealer():
#     for key in list(cars_models.keys()):
#         for j in range(5):
#             bmw_car = Car.objects.create(name=key,
#                                          model=f"Model {random.choice(list(cars_models[key]))}",
#                                          body_type=get_random_body_type(),
#                                          transmission_type=get_random_transmission(),
#                                          color=get_random_color(),
#                                          year=get_random_year(),
#                                          price=random.randint(5000, 15000),
#                                          dealer=Dealer.objects.get(name=f"{key} Dealer"))
#
#     print('Added cars for dealers')


class Command(BaseCommand):
    help = u'Add dealers and cars for them'

    def handle(self, *args, **options):
        add_dealers()
        # add_cars_for_dealer()
        return 'Done'
