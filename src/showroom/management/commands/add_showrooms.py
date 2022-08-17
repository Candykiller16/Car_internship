from django.core.management.base import BaseCommand

from core.data_and_funcs import districts
from src.users.models import CustomUser


def add_showrooms():
    for i in districts:
        showrooms = CustomUser.objects.create_user(username=f'{i.lower()}_showroom', first_name=f'{i} Showroom',
                                                   email=f'{i.lower()}_showroom@mail.ru', password='123',
                                                   is_superuser=False,
                                                   is_staff=False, is_showroom=True)

    print('Added showrooms')


class Command(BaseCommand):
    help = u'Add showrooms and cars for them'

    def handle(self, *args, **options):
        add_showrooms()
        # add_cars_for_showroom()
        return 'Done'
