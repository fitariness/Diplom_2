import allure

import config
from api.stellar_burgers_api import StellarBurgersApi
from tests.helpers.checkers import (
    check_invalid_ingredient_hash_error,
    check_ingredients_required_error,
    check_order_created_success,
    check_order_created_without_name,
)


@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_auth_and_ingredients(
        self, api: StellarBurgersApi, registered_user, ingredient_ids: list[str]
    ):
        """Проверка создания заказа авторизованным пользователем"""
        response = api.create_order_with_auth(
            ingredient_ids=ingredient_ids,
            access_token=registered_user['access_token'],
        )
        check_order_created_success(response)

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_auth(
        self, api: StellarBurgersApi, ingredient_ids: list[str]
    ):
        """Проверка создания заказа без авторизации"""
        response = api.create_order_without_auth(ingredient_ids=ingredient_ids)
        check_order_created_without_name(response)

    @allure.title('Создание заказа с ингредиентами')
    def test_create_order_with_ingredients(
        self, api: StellarBurgersApi, registered_user, ingredient_ids: list[str]
    ):
        """Проверка создания заказа, если переданы валидные ингредиенты"""
        response = api.create_order_with_auth(
            ingredient_ids=ingredient_ids,
            access_token=registered_user['access_token'],
        )
        check_order_created_success(response)

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients_bad_request(
        self, api: StellarBurgersApi, registered_user
    ):
        """Проверка ошибки при создании заказа без ингредиентов"""
        response = api.create_order_with_auth(
            ingredient_ids=[],
            access_token=registered_user['access_token'],
        )
        check_ingredients_required_error(response)

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredient_hash_server_error(
        self, api: StellarBurgersApi, registered_user
    ):
        """Проверка ошибки при невалидном хеше ингредиента"""
        response = api.create_order_with_auth(
            ingredient_ids=[config.INVALID_INGREDIENT_HASH],
            access_token=registered_user['access_token'],
        )
        check_invalid_ingredient_hash_error(response)
