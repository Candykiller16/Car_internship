import pytest


@pytest.mark.django_db
def test_showroom_get_list(auth_admin, auth_user_is_showroom, auth_user_is_showroom2, auth_user_not_showroom,
                           get_responses, client):
    """
    Ensure that only ADMIN can get a list of Showrooms.
    """
    url = '/api/showroom/'
    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_showroom, url=url) == 403
    assert get_responses(client=auth_user_is_showroom, url=url) == 403
    assert get_responses(client=auth_user_is_showroom2, url=url) == 403


@pytest.mark.django_db
def test_showroom_get_me(auth_admin, auth_user_is_showroom, auth_user_is_showroom2, auth_user_not_showroom,
                         get_responses, client):
    """
    Ensure that only OWNER OF SHOWROOM OBJECT can see info.
    """
    url = '/api/showroom/me/'
    assert get_responses(client=auth_admin, url=url) == 403
    assert get_responses(client=auth_user_not_showroom, url=url) == 403
    assert get_responses(client=auth_user_is_showroom, url=url) == 200
    assert get_responses(client=auth_user_is_showroom2, url=url) == 200


@pytest.mark.django_db
def test_showroom_see_others_showroom_info(auth_admin, auth_user_is_showroom, auth_user_is_showroom2,
                                           auth_user_not_showroom, user_is_showroom, get_responses, client):
    """
    Ensure that only Admin can see detail info of every showroom.
    """
    url = f'/api/showroom/{user_is_showroom.showroom.id}/'

    assert get_responses(client=auth_admin, url=url) == 200
    assert get_responses(client=auth_user_not_showroom, url=url) == 403
    assert get_responses(client=auth_user_is_showroom, url=url) == 403
    assert get_responses(client=auth_user_is_showroom2, url=url) == 403


@pytest.mark.django_db
def test_dealer_update_others_showroom_info(auth_admin, auth_user_is_showroom, auth_user_is_showroom2,
                                            auth_user_not_showroom, user_is_showroom, put_responses, client):
    """
    Ensure that OWNER OF DEALER OBJECT can update info about him.
    """
    url = f'/api/showroom/me/'
    payload = {
        "name": "Kirill ",
        "email": "kirill@mail.ru"
    }
    assert put_responses(client=auth_admin, url=url, update_payload=payload) == 403
    assert put_responses(client=auth_user_is_showroom, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_is_showroom2, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_not_showroom, url=url, update_payload=payload) == 403


@pytest.mark.django_db
def test_admin_update_others_showroom_info(auth_admin, auth_user_is_showroom, auth_user_is_showroom2,
                                           auth_user_not_showroom, user_is_showroom, put_responses, client):
    """
    Ensure that Admin can update info about every showroom.
    """
    url = f'/api/showroom/{user_is_showroom.showroom.id}/'
    payload = {
        "name": "Kirill ",
        "email": "kirill@mail.ru"
    }
    assert put_responses(client=auth_admin, url=url, update_payload=payload) == 200
    assert put_responses(client=auth_user_is_showroom, url=url, update_payload=payload) == 403
    assert put_responses(client=auth_user_is_showroom2, url=url, update_payload=payload) == 403
    assert put_responses(client=auth_user_not_showroom, url=url, update_payload=payload) == 403
