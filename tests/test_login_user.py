import allure

from api.stellar_burgers_api import StellarBurgersApi
from tests.helpers.checkers import check_incorrect_credentials, check_login_success
from tests.helpers.data import unique_email


@allure.feature('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Вход под существующим пользователем')
    def test_login_existing_user_success(self, api: StellarBurgersApi, registered_user):
        """Проверка успешного входа зарегистрированного пользователя"""
        response = api.login_user(
            email=registered_user['email'],
            password=registered_user['password'],
        )
        check_login_success(response, registered_user)

    @allure.title('Вход с неверным логином и паролем')
    def test_login_with_invalid_credentials_unauthorized(self, api: StellarBurgersApi):
        """Проверка ошибки входа с неверными учётными данными"""
        response = api.login_user(email=unique_email(), password='wrong_password')
        check_incorrect_credentials(response)
