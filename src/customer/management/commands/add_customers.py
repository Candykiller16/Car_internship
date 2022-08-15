from django.core.management.base import BaseCommand

from core.data_and_funcs import *
from src.customer.models import Customer, CustomerOffer
from src.users.models import CustomUser


def add_customers():
    for person in customer_list:
        customers = CustomUser.objects.create_user(username=f"{person.lower().replace(' ', '_')}",
                                                   first_name=f'{person}',
                                                   email=f"{person.lower().replace(' ', '_')}@mail.ru",
                                                   password='123',
                                                   is_superuser=False,
                                                   is_staff=False, is_customer=True)


def add_offers_for_customers():
    for person in Customer.objects.all():
        for i in range(1):
            dictionary = get_random_name_and_model()
            offer = CustomerOffer.objects.create(
                customer=person,
                selected_car={
                    "name": list(dictionary.keys())[0],
                    "model": list(dictionary.values())[0],
                    "body_type": get_random_body_type(),
                    "transmission_type": get_random_transmission(),
                    "color": get_random_color(),
                    "year": get_random_year(),
                    "price": random.randint(10000, 30000),
                }
            )


class Command(BaseCommand):
    help = u'Add users'

    def handle(self, *args, **options):
        add_customers()
        add_offers_for_customers()
        return 'Done'
