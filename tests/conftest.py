import pytest

from api.stellar_burgers_api import StellarBurgersApi
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
