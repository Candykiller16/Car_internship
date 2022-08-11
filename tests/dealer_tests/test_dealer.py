import pytest


@pytest.mark.django_db
def test_dealer_get_list(auth_user_is_dealer1, get_responses, auth_user_is_dealer2, auth_admin, auth_user_not_dealer):
    """
    Ensure that only ADMIN can get a list of Dealers.
    """
    url = '/api/dealer/'
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_dealer, url=url) == 403
    assert get_responses(client=auth_user_is_dealer1, url=url) == 403
    assert get_responses(client=auth_user_is_dealer2, url=url) == 403


@pytest.mark.django_db
def test_dealer_get_me(auth_user_not_dealer, auth_admin, auth_user_is_dealer1, auth_user_is_dealer2, get_responses,
                       client):
    """
    Ensure that only OWNER OF DEALER OBJECT can see info.
    """
    url = '/api/dealer/me/'
    assert get_responses(client=auth_admin, url=url) == 403
    assert get_responses(client=auth_user_not_dealer, url=url) == 403
    assert get_responses(client=auth_user_is_dealer1, url=url) == 200
    assert get_responses(client=auth_user_is_dealer2, url=url) == 200


@pytest.mark.django_db
def test_dealer_see_others_dealer_info(auth_user_not_dealer, auth_admin, auth_user_is_dealer1, auth_user_is_dealer2,
                                       get_responses, user_is_dealer1):
    """
    Ensure that only Admin can see detail info of every dealer.
    """
    url = f'/api/dealer/{user_is_dealer1.dealer.id}/'

    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_dealer, url=url) == 403
    assert get_responses(client=auth_user_is_dealer1, url=url) == 403
    assert get_responses(client=auth_user_is_dealer2, url=url) == 403


@pytest.mark.django_db
def test_dealer_update_others_dealer_info(auth_user_not_dealer, auth_admin, auth_user_is_dealer1, auth_user_is_dealer2,
                                          put_responses):
    """
    Ensure that OWNER OF DEALER OBJECT can update info about him.
    """
    url = f'/api/dealer/me/'
    payload = {
        "name": "Kirill ",
        "email": "kirill@mail.ru"
    }
    assert put_responses(client=auth_admin, url=url, update_payload=payload) == 403
    assert put_responses(client=auth_user_is_dealer1, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_is_dealer2, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_not_dealer, url=url, update_payload=payload) == 403


@pytest.mark.django_db
def test_admin_update_others_dealer_info(auth_user_not_dealer, auth_admin, auth_user_is_dealer1, auth_user_is_dealer2,
                                         user_is_dealer1, put_responses,
                                         client):
    """
    Ensure that Admin can update info about every dealer.
    """
    url = f'/api/dealer/{user_is_dealer1.dealer.id}/'
    payload = {
        "name": "Kirill ",
        "email": "kirill@mail.ru"
    }
    assert put_responses(client=auth_admin, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_is_dealer1, url=url, update_payload=payload) == 403
    assert put_responses(client=auth_user_is_dealer2, url=url, update_payload=payload) == 403
    assert put_responses(client=auth_user_not_dealer, url=url, update_payload=payload) == 403
