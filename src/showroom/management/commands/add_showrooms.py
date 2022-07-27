from django.core.management.base import BaseCommand

from src.users.models import CustomUser
from core.data_and_funcs import districts


def add_showrooms():
    for i in districts:
        showrooms = CustomUser.objects.create_user(username=f'{i.lower()}_showroom', first_name=f'{i} Showroom',
                                                   email=f'{i.lower()}_showroom@mail.ru', password='123',
                                                   is_superuser=False,
                                                   is_staff=False, is_showroom=True)

    print('Added showrooms')


# def add_cars_for_showroom():
#     for district in districts:
#         for i in range(5):
#             cars = Car.objects.create(name=list(get_random_key_and_value().keys())[0],
#                                       model=f"Model {list(get_random_key_and_value().values())[0]}",
#                                       body_type=get_random_body_type(),
#                                       transmission_type=get_random_transmission(),
#                                       color=get_random_color(),
#                                       year=get_random_year(),
#                                       price=random.randint(5000, 15000),
#                                       showroom=Showroom.objects.get(name=f"{district} Showroom"))
#
#     print('Added cars for showroom')


class Command(BaseCommand):
    help = u'Add showrooms and cars for them'

    def handle(self, *args, **options):
        add_showrooms()
        # add_cars_for_showroom()
        return 'Done'
