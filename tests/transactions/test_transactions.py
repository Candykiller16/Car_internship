import pytest


@pytest.mark.django_db
def test_get_transactions_from_dealer_to_showroom(transactions_dealer_showroom,
                                                  get_responses, auth_admin,
                                                  auth_user_is_dealer1,
                                                  auth_user_is_showroom,
                                                  auth_user_is_showroom2,
                                                  auth_user_is_customer1,
                                                  auth_user_not_dealer):
    """
    Ensure that only ADMIN can get a list of all Transactions.
    Dealer and Showroom can only view transactions related to them .
    """

    url = '/api/dealer_showroom/'
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_is_dealer1, url=url) == 200
    assert get_responses(client=auth_user_is_showroom, url=url) == 200
    assert get_responses(client=auth_user_is_showroom2, url=url) == 200
    assert get_responses(client=auth_user_is_customer1, url=url) == 403
    assert get_responses(client=auth_user_not_dealer, url=url) == 403


@pytest.mark.django_db
def test_get_transaction_from_dealer_to_showroom(
        transactions_dealer_showroom,
        get_responses, auth_admin,
        auth_user_is_dealer1,
        auth_user_is_showroom,
        auth_user_is_showroom2,
        auth_user_is_customer1,
        auth_user_not_dealer
):
    """
    Ensure that only ADMIN can get any separately Transaction.
    Dealer and Showroom can only view transactions related to them .
    """

    url = f'/api/dealer_showroom/{transactions_dealer_showroom.id}/'

    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_is_dealer1, url=url) == 200
    assert get_responses(client=auth_user_is_showroom, url=url) == 200
    assert get_responses(client=auth_user_is_showroom2, url=url) == 403
    assert get_responses(client=auth_user_is_customer1, url=url) == 403
    assert get_responses(client=auth_user_not_dealer, url=url) == 403


@pytest.mark.django_db
def test_get_transactions_from_showroom_to_customer(
        transactions_showroom_customer,
        get_responses, auth_admin,
        auth_user_is_customer1,
        auth_user_is_showroom,
        auth_user_is_showroom2,
        auth_user_is_dealer1,
        auth_user_not_dealer
):
    """
    Ensure that only ADMIN can get a list of all Transactions.
    Showroom and Customer can only view transactions related to them .
    """

    url = '/api/showroom_customer/'
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_is_customer1, url=url) == 200
    assert get_responses(client=auth_user_is_showroom, url=url) == 200
    assert get_responses(client=auth_user_is_showroom2, url=url) == 200
    assert get_responses(client=auth_user_is_dealer1, url=url) == 403
    assert get_responses(client=auth_user_not_dealer, url=url) == 403


@pytest.mark.django_db
def test_get_transaction_from_showroom_to_customer(
        transactions_showroom_customer,
        get_responses, auth_admin,
        auth_user_is_customer1,
        auth_user_is_showroom,
        auth_user_is_showroom2,
        auth_user_is_dealer1,
        auth_user_not_dealer
):
    """
    Ensure that only ADMIN can get a list of all Transactions.
    Showroom and Customer can only view transactions related to them .
    """

    url = f'/api/showroom_customer/{transactions_showroom_customer.id}/'
    response = auth_admin.get(url)
    print(response.json())
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_is_customer1, url=url) == 200
    assert get_responses(client=auth_user_is_showroom, url=url) == 200
    assert get_responses(client=auth_user_is_showroom2, url=url) == 403
    assert get_responses(client=auth_user_is_dealer1, url=url) == 403
    assert get_responses(client=auth_user_not_dealer, url=url) == 403
