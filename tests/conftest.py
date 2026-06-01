import pytest

from api.stellar_burgers_api import StellarBurgersApi
from tests.helpers.data import default_user_payload
from tests.helpers.ingredient import get_ingredient_ids
from tests.helpers.user import create_registered_user, delete_registered_user


@pytest.fixture
def api() -> StellarBurgersApi:
    return StellarBurgersApi()


@pytest.fixture
def ingredient_ids(api: StellarBurgersApi) -> list[str]:
    return get_ingredient_ids(api)


@pytest.fixture
def registered_user(api: StellarBurgersApi):
    user_data = create_registered_user(api)
    yield user_data
    delete_registered_user(api, user_data['access_token'])


@pytest.fixture
def new_user_registration(api: StellarBurgersApi):
    payload = default_user_payload()
    response = api.register_user(payload)
    yield {'payload': payload, 'response': response}

    body = response.json()
    access_token = body.get('accessToken')
    if access_token:
        delete_registered_user(api, access_token)
