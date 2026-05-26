from api.stellar_burgers_api import StellarBurgersApi
from tests.helpers.data import default_user_payload


def create_registered_user(api: StellarBurgersApi) -> dict:
    payload = default_user_payload()
    response = api.register_user(**payload)
    body = response.json()
    return {
        'email': payload['email'],
        'password': payload['password'],
        'name': payload['name'],
        'access_token': body['accessToken'],
    }


def delete_registered_user(api: StellarBurgersApi, access_token: str) -> None:
    api.delete_user(access_token)
