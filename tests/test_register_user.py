import allure
import pytest

from api.stellar_burgers_api import StellarBurgersApi
from tests.helpers.checkers import (
    check_register_success,
    check_required_fields_error,
    check_user_already_exists,
)
from tests.helpers.data import default_user_payload, user_payload_without_field
from tests.helpers.user import delete_registered_user


@allure.feature('Регистрация пользователя')
class TestRegisterUser:
    @allure.title('Создание уникального пользователя')
    def test_register_unique_user_success(self, api: StellarBurgersApi):
        """Проверка успешной регистрации нового уникального пользователя"""
        payload = default_user_payload()
        response = api.register_user(**payload)
        access_token = check_register_success(response, payload)
        delete_registered_user(api, access_token)

    @allure.title('Создание уже зарегистрированного пользователя')
    def test_register_existing_user_forbidden(self, api: StellarBurgersApi, registered_user):
        """Проверка ошибки при повторной регистрации существующего пользователя"""
        response = api.register_user(
            email=registered_user['email'],
            password=registered_user['password'],
            name=registered_user['name'],
        )
        check_user_already_exists(response)

    @allure.title('Создание пользователя без обязательного поля')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_register_user_without_required_field(
        self, api: StellarBurgersApi, missing_field: str
    ):
        """Проверка ошибки, если не передано одно обязательное поле"""
        payload = user_payload_without_field(missing_field)
        response = api.register_user_payload(payload)
        check_required_fields_error(response)
