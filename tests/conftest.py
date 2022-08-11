import pytest
from rest_framework.test import APIClient

from src.car.models import Car
from src.customer.models import CustomerOffer
from src.showroom.models import Showroom
from src.transaction.models import FromDealerToShowroomTransaction, FromShowroomToCustomerTransaction
from src.users.models import CustomUser


@pytest.fixture()
def auth_admin():
    admin = CustomUser.objects.create_user(username='admin',
                                           password='admin',
                                           first_name='Anton Admin',
                                           is_superuser=True,
                                           is_staff=True, )
    auth_client = APIClient()
    auth_client.force_login(admin)
    return auth_client


@pytest.fixture()
def user_is_customer1():
    customer = CustomUser.objects.create_user(username='customer3',
                                              password='customer3',
                                              first_name='Anton Customer3',
                                              is_customer=True)
    return customer


@pytest.fixture()
def user_is_customer2():
    customer = CustomUser.objects.create_user(username='customer4',
                                              password='customer4',
                                              first_name='Anton Customer4',
                                              is_customer=True)
    return customer


@pytest.fixture()
def auth_user_is_customer1(user_is_customer1):
    auth_client = APIClient()
    auth_client.force_login(user_is_customer1)
    return auth_client


@pytest.fixture()
def auth_user_is_customer2(user_is_customer2):
    auth_client = APIClient()
    auth_client.force_login(user_is_customer2)
    return auth_client


@pytest.fixture()
def auth_user_not_customer():
    not_customer = CustomUser.objects.create_user(username='not_customer',
                                                  password='not_customer',
                                                  first_name='Anton NotCustomer',
                                                  is_customer=False)
    auth_client = APIClient()
    auth_client.force_login(not_customer)
    return auth_client


@pytest.fixture()
def customer_offer(user_is_customer1, selected_car):
    customer_offer = CustomerOffer.objects.create(
        customer=user_is_customer1.customer,
        price=2005,
        selected_car=selected_car,
        is_active=True,
    )
    return customer_offer


@pytest.fixture()
def create_car():
    car = Car.objects.create(
        name="BMW",
        model="Model I",
        color="Red",
        price=12000.00,
    )
    return car


@pytest.fixture()
def selected_car():
    return {
        "make": "BMW",
        "model": "Model I",
        "color": "Red",
        "year": "2010",
        "body_type": "Sedan"
    }


@pytest.fixture()
def updated_car():
    return {
        "make": "Audi",
        "model": "Model II",
        "color": "Blue",
        "year": "2020",
        "body_type": "Sedan"
    }


@pytest.fixture
def user_is_dealer1():
    dealer = CustomUser.objects.create_user(username='dealer3',
                                            password='dealer3',
                                            first_name='Anton Dealer3',
                                            is_dealer=True)
    return dealer


@pytest.fixture
def auth_user_is_dealer1(user_is_dealer1):
    auth_client = APIClient()
    auth_client.force_login(user_is_dealer1)
    return auth_client


@pytest.fixture
def user_is_dealer2():
    dealer = CustomUser.objects.create_user(username='dealer5',
                                            password='dealer5',
                                            first_name='Anton Dealer5',
                                            is_dealer=True)
    return dealer


@pytest.fixture
def auth_user_is_dealer2(user_is_dealer2):
    auth_client = APIClient()
    auth_client.force_login(user_is_dealer2)
    return auth_client


@pytest.fixture
def auth_user_not_dealer():
    not_dealer = CustomUser.objects.create_user(username='not_dealer',
                                                password='not_dealer',
                                                first_name='Anton NotDealer',
                                                is_dealer=False)
    auth_client = APIClient()
    auth_client.force_login(not_dealer)
    return auth_client


@pytest.fixture()
def user_is_showroom():
    showroom = CustomUser.objects.create_user(username='showroom3',
                                              password='showroom3',
                                              first_name='Anton Showroom3',
                                              is_showroom=True)
    return showroom


@pytest.fixture()
def auth_user_is_showroom(user_is_showroom):
    auth_client = APIClient()
    auth_client.force_login(user_is_showroom)
    return auth_client


@pytest.fixture()
def auth_user_is_showroom2():
    showroom2 = CustomUser.objects.create_user(username='showroom2',
                                               password='showroom2',
                                               first_name='Anton Showroom2',
                                               is_showroom=True)
    auth_client = APIClient()
    auth_client.force_login(showroom2)
    return auth_client


@pytest.fixture()
def auth_user_not_showroom():
    not_showroom = CustomUser.objects.create_user(username='not_showroom',
                                                  password='not_showroom',
                                                  first_name='Anton NotShowroom',
                                                  is_showroom=False)
    auth_client = APIClient()
    auth_client.force_login(not_showroom)
    return auth_client


@pytest.fixture()
def transactions_dealer_showroom(user_is_dealer1, create_car, user_is_showroom):
    transactions = FromDealerToShowroomTransaction.objects.create(
        dealer=user_is_dealer1.dealer,
        showroom=user_is_showroom.showroom,
        car=create_car,
        discount=0,
        price=15000,
    )
    return transactions


@pytest.fixture()
def transactions_showroom_customer(user_is_customer1, create_car, user_is_showroom):
    transactions = FromShowroomToCustomerTransaction.objects.create(
        showroom=user_is_showroom.showroom,
        customer=user_is_customer1.customer,
        car=create_car,
        discount=0,
        price=15000,
    )
    return transactions


def _get_responses(client, url):
    return client.get(url).status_code


@pytest.fixture
def get_responses():
    return _get_responses


def _put_responses(client, url, update_payload):
    return client.put(url, update_payload, format='json').status_code


@pytest.fixture
def put_responses():
    return _put_responses


def _post_responses(client, url, post_data):
    return client.post(url, post_data, format='json').status_code


@pytest.fixture
def post_responses():
    return _post_responses


def _deactivate_responses(client, url):
    return client.put(url, format='json').status_code


@pytest.fixture
def deactivate_responses():
    return _deactivate_responses


def _activate_responses(client, url):
    return client.put(url, format='json').status_code


@pytest.fixture
def activate_responses():
    return _activate_responses
