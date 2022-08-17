from django.core.management.base import BaseCommand

from core.data_and_funcs import cars_models
from src.users.models import CustomUser


def add_dealers():
    for key in list(cars_models):
        dealers = CustomUser.objects.create_user(username=f'{key}_dealer',
                                                 first_name=f'{key} Dealer',
                                                 email=f'{key}@mail.ru', password='123',
                                                 is_superuser=False,
                                                 is_staff=False, is_dealer=True)

    print('Added dealers')


class Command(BaseCommand):
    help = u'Add dealers and cars for them'

    def handle(self, *args, **options):
        add_dealers()
        return 'Done'
