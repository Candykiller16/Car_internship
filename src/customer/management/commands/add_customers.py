from django.core.management.base import BaseCommand
from core.data_and_funcs import customer_list
from src.users.models import CustomUser


def add_customers():
    for person in customer_list:
        customers = CustomUser.objects.create_user(username=f"{person.lower().replace(' ', '_')}",
                                                   first_name=f'{person}',
                                                   email=f"{person.lower().replace(' ', '_')}@mail.ru",
                                                   password='123',
                                                   is_superuser=False,
                                                   is_staff=False, is_customer=True)


class Command(BaseCommand):
    help = u'Add users'

    def handle(self, *args, **options):
        add_customers()
        return 'Done'
