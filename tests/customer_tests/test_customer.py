import pytest


@pytest.mark.django_db
def test__get_list_of_customers(auth_user_not_customer, auth_admin, auth_user_is_customer1, auth_user_is_customer2,
                                get_responses, client):
    """
    Ensure that only ADMIN can get a list of Customers.
    """
    url = '/api/customer/'
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_customer, url=url) == 403
    assert get_responses(client=auth_user_is_customer1, url=url) == 403
    assert get_responses(client=auth_user_is_customer2, url=url) == 403


#

@pytest.mark.django_db
def test_customer_get_me(auth_user_not_customer, auth_admin, auth_user_is_customer1, auth_user_is_customer2,
                         get_responses, client):
    """
    Ensure that only OWNER OF CUSTOMER OBJECT can see info.
    """
    url = '/api/customer/me/'
    assert get_responses(client=auth_admin, url=url) == 403
    assert get_responses(client=auth_user_not_customer, url=url) == 403
    assert get_responses(client=auth_user_is_customer1, url=url) == 200
    assert get_responses(client=auth_user_is_customer2, url=url) == 200


@pytest.mark.django_db
def test_see_dealer_detail(auth_user_not_customer, auth_admin, auth_user_is_customer1,
                           auth_user_is_customer2, user_is_customer1, get_responses, client):
    """
    Ensure that only Admin can see detail info of every customer.
    """
    url = f'/api/customer/{user_is_customer1.customer.id}/'

    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_customer, url=url) == 403
    assert get_responses(client=auth_user_is_customer1, url=url) == 403
    assert get_responses(client=auth_user_is_customer2, url=url) == 403


@pytest.mark.django_db
def test_update_customer_info(auth_user_not_customer, auth_admin, auth_user_is_customer1,
                              auth_user_is_customer2, put_responses):
    """
    Ensure that OWNER OF CUSTOMER OBJECT can update info about him.
    """
    url = f'/api/customer/me/'
    payload = {
        "name": "Kirill ",
        "email": "kirill@mail.ru"
    }
    assert put_responses(client=auth_admin, url=url, update_payload=payload) == 403
    assert put_responses(client=auth_user_is_customer1, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_is_customer2, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_not_customer, url=url, update_payload=payload) == 403


@pytest.mark.django_db
def test_customer_offer__should_return_created(auth_user_is_customer1, auth_admin, auth_user_not_customer,
                                               selected_car, client, post_responses):
    """
    Ensure that only Customer can create Customer Offer
    """

    payload = {
        "price": 2000.00,
        "selected_car": selected_car
    }
    url = '/api/customer_offer/'
    assert post_responses(client=auth_user_is_customer1, url=url, post_data=payload) == 201
    assert post_responses(client=auth_admin, url=url, post_data=payload) == 403
    assert post_responses(client=auth_user_not_customer, url=url, post_data=payload) == 403


@pytest.mark.django_db
def test_get_offer_by_is_customer(auth_admin, auth_user_is_customer1, auth_user_is_customer2,
                                  customer_offer, auth_user_not_customer, get_responses):
    """
    Ensure that OWNER OF CUSTOMER OFFER can see his offer. And Admin too.
    """
    url = f'/api/customer_offer/{customer_offer.id}/'

    assert get_responses(client=auth_user_is_customer1, url=url) == 200
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_is_customer2, url=url) == 403
    assert get_responses(client=auth_user_not_customer, url=url) == 403


@pytest.mark.django_db
def test_update_offer_by_is_customer(auth_admin, auth_user_is_customer1, auth_user_is_customer2, updated_car,
                                     customer_offer, auth_user_not_customer, put_responses):
    """
    Ensure that OWNER OF CUSTOMER OFFER can update his offer. And Admin too.
    """

    payload = {
        "price": 3000.00,
        "selected_car": updated_car,
    }
    url = f'/api/customer_offer/{customer_offer.id}/'

    assert put_responses(client=auth_user_is_customer1, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_admin, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_is_customer2, url=url, update_payload=payload) == 403
    assert put_responses(client=auth_user_not_customer, url=url, update_payload=payload) == 403


@pytest.mark.django_db
def test_deactivate_offer(auth_admin, auth_user_is_customer1, auth_user_is_customer2, customer_offer,
                          auth_user_not_customer, put_responses, deactivate_responses):
    url = f'/api/customer_offer/{customer_offer.id}/deactivate/'

    assert deactivate_responses(client=auth_user_is_customer1, url=url) == 200
    assert deactivate_responses(client=auth_admin, url=url) == 200
    assert deactivate_responses(client=auth_user_is_customer2, url=url) == 403
    assert deactivate_responses(client=auth_user_not_customer, url=url) == 403


@pytest.mark.django_db
def test_activate_offer(auth_admin, auth_user_is_customer1, auth_user_is_customer2, customer_offer,
                        auth_user_not_customer, put_responses, activate_responses, deactivate_responses):
    """
    Ensure that ONLY OWNER OF OFFER OBJECT or Admin can activate deactivated offer
    """

    url = f'/api/customer_offer/{customer_offer.id}/activate/'

    assert deactivate_responses(client=auth_user_is_customer1, url=url) == 200
    assert activate_responses(client=auth_user_is_customer1, url=url) == 200
    assert deactivate_responses(client=auth_user_is_customer1, url=url) == 200
    assert activate_responses(client=auth_admin, url=url) == 200
    assert deactivate_responses(client=auth_user_is_customer1, url=url) == 200
    assert activate_responses(client=auth_user_is_customer2, url=url) == 403
    assert deactivate_responses(client=auth_user_is_customer1, url=url) == 200
    assert activate_responses(client=auth_user_not_customer, url=url) == 403


@pytest.mark.django_db
def test_to_see_dealers(auth_admin, auth_user_is_customer1, auth_user_is_customer2, auth_user_not_customer,
                        auth_user_is_dealer1, user_is_dealer1, user_is_dealer2, get_responses):
    """
    Ensure that only Customer and Admin can see all dealers
    """
    url = '/api/dealer/'
    assert get_responses(client=auth_user_is_customer1, url=url) == 200
    assert get_responses(client=auth_user_is_customer2, url=url) == 200
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_customer, url=url) == 403
    assert get_responses(client=auth_user_is_dealer1, url=url) == 403


@pytest.mark.django_db
def test_to_see_dealers(auth_admin, auth_user_is_customer1, auth_user_is_customer2, auth_user_not_customer,
                        auth_user_is_dealer1, user_is_dealer1, user_is_dealer2, get_responses):
    """
    Ensure that only Customer and Admin can see detail dealer
    """
    url = f'/api/dealer/{user_is_dealer1.dealer.id}/'
    assert get_responses(client=auth_user_is_customer1, url=url) == 200
    assert get_responses(client=auth_user_is_customer2, url=url) == 200
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_customer, url=url) == 403
    assert get_responses(client=auth_user_is_dealer1, url=url) == 403


@pytest.mark.django_db
def test_to_see_dealers(auth_admin, auth_user_is_customer1, auth_user_is_customer2, auth_user_not_customer,
                        auth_user_is_dealer1, user_is_dealer1, user_is_dealer2, get_responses):
    """
    Ensure that only Customer and Admin can see showrooms
    """
    url = f'/api/showroom/'
    assert get_responses(client=auth_user_is_customer1, url=url) == 200
    assert get_responses(client=auth_user_is_customer2, url=url) == 200
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_customer, url=url) == 403
    assert get_responses(client=auth_user_is_dealer1, url=url) == 403


@pytest.mark.django_db
def test_to_see_dealers(auth_admin, auth_user_is_customer1, auth_user_is_customer2, auth_user_not_customer,
                        auth_user_is_dealer1, user_is_dealer1, user_is_dealer2, get_responses, user_is_showroom):
    """
    Ensure that only Customer and Admin can see showrooms
    """
    url = f'/api/showroom/{user_is_showroom.showroom.id}/'
    assert get_responses(client=auth_user_is_customer1, url=url) == 200
    assert get_responses(client=auth_user_is_customer2, url=url) == 200
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_customer, url=url) == 403
    assert get_responses(client=auth_user_is_dealer1, url=url) == 403
