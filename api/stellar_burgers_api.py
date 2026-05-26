import allure
import requests

import config


class StellarBurgersApi:
    def __init__(self, base_url: str = config.BASE_URL):
        self.base_url = base_url

    def _url(self, endpoint: str) -> str:
        return f'{self.base_url}{endpoint}'

    @allure.step('POST /auth/register - регистрация пользователя')
    def register_user(self, email: str, password: str, name: str) -> requests.Response:
        return self.register_user_payload(
            {'email': email, 'password': password, 'name': name}
        )

    @allure.step('POST /auth/register - регистрация пользователя (произвольное тело)')
    def register_user_payload(self, payload: dict) -> requests.Response:
        return requests.post(self._url(config.REGISTER_ENDPOINT), json=payload)

    @allure.step('POST /auth/login - авторизация пользователя')
    def login_user(self, email: str, password: str) -> requests.Response:
        return requests.post(
            self._url(config.LOGIN_ENDPOINT),
            json={'email': email, 'password': password},
        )

    @allure.step('DELETE /auth/user - удаление пользователя')
    def delete_user(self, access_token: str) -> requests.Response:
        return requests.delete(
            self._url(config.USER_ENDPOINT),
            headers={'Authorization': access_token},
        )

    @allure.step('GET /ingredients - получение списка ингредиентов')
    def get_ingredients(self) -> requests.Response:
        return requests.get(self._url(config.INGREDIENTS_ENDPOINT))

    @allure.step('POST /orders - создание заказа с авторизацией')
    def create_order_with_auth(
        self, ingredient_ids: list[str], access_token: str
    ) -> requests.Response:
        return requests.post(
            self._url(config.ORDERS_ENDPOINT),
            json={'ingredients': ingredient_ids},
            headers={'Authorization': access_token},
        )

    @allure.step('POST /orders - создание заказа без авторизации')
    def create_order_without_auth(self, ingredient_ids: list[str]) -> requests.Response:
        return requests.post(
            self._url(config.ORDERS_ENDPOINT),
            json={'ingredients': ingredient_ids},
        )
