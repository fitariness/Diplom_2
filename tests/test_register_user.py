import allure
import pytest

from api.stellar_burgers_api import StellarBurgersApi
from tests.helpers.checkers import (
    check_register_success,
    check_required_fields_error,
    check_user_already_exists,
)
from tests.helpers.data import user_payload_without_field


@allure.feature('Регистрация пользователя')
class TestRegisterUser:
    @allure.title('Создание уникального пользователя')
    def test_register_unique_user_success(self, new_user_registration):
        """Проверка успешной регистрации нового уникального пользователя"""
        payload = new_user_registration['payload']
        response = new_user_registration['response']
        check_register_success(response, payload)

    @allure.title('Создание уже зарегистрированного пользователя')
    def test_register_existing_user_forbidden(self, api: StellarBurgersApi, registered_user):
        """Проверка ошибки при повторной регистрации существующего пользователя"""
        response = api.register_user_with_required_fields(
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
        response = api.register_user(payload)
        check_required_fields_error(response)
