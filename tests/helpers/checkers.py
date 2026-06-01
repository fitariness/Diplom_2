import allure
import requests

import config


@allure.step('Проверить статус-код ответа: {expected_code}')
def check_status_code(response: requests.Response, expected_code: int) -> None:
    """Проверка HTTP-статуса ответа"""
    assert response.status_code == expected_code


@allure.step('Проверить успешную регистрацию пользователя')
def check_register_success(response: requests.Response, payload: dict) -> None:
    """Проверка тела ответа при успешной регистрации"""
    check_status_code(response, 200)
    body = response.json()
    assert body['success'] is True
    assert body['user']['email'] == payload['email']
    assert body['user']['name'] == payload['name']
    assert body['accessToken'].startswith('Bearer ')
    assert body['refreshToken']


@allure.step('Проверить ошибку: пользователь уже существует')
def check_user_already_exists(response: requests.Response) -> None:
    """Проверка ответа при повторной регистрации пользователя"""
    check_status_code(response, 403)
    body = response.json()
    assert body['success'] is False
    assert body['message'] == config.MSG_USER_ALREADY_EXISTS


@allure.step('Проверить ошибку: не заполнены обязательные поля')
def check_required_fields_error(response: requests.Response) -> None:
    """Проверка ответа при отсутствии обязательного поля"""
    check_status_code(response, 403)
    body = response.json()
    assert body['success'] is False
    assert body['message'] == config.MSG_REQUIRED_FIELDS


@allure.step('Проверить успешный логин пользователя')
def check_login_success(response: requests.Response, expected_user: dict) -> None:
    """Проверка тела ответа при успешной авторизации"""
    check_status_code(response, 200)
    body = response.json()
    assert body['success'] is True
    assert body['accessToken'].startswith('Bearer ')
    assert body['refreshToken']
    assert body['user']['email'] == expected_user['email']
    assert body['user']['name'] == expected_user['name']


@allure.step('Проверить ошибку: неверный логин или пароль')
def check_incorrect_credentials(response: requests.Response) -> None:
    """Проверка ответа при неверных учётных данных"""
    check_status_code(response, 401)
    body = response.json()
    assert body['success'] is False
    assert body['message'] == config.MSG_INCORRECT_CREDENTIALS


@allure.step('Проверить успешное создание заказа')
def check_order_created_success(response: requests.Response) -> None:
    """Проверка тела ответа при успешном создании заказа"""
    check_status_code(response, 200)
    body = response.json()
    assert body['success'] is True
    assert body['order']['number'] > 0
    assert body['name']


@allure.step('Проверить успешное создание заказа (без проверки name)')
def check_order_created_without_name(response: requests.Response) -> None:
    """Проверка успешного заказа, когда в ответе не нужен name"""
    check_status_code(response, 200)
    body = response.json()
    assert body['success'] is True
    assert body['order']['number'] > 0


@allure.step('Проверить ошибку: не переданы ингредиенты')
def check_ingredients_required_error(response: requests.Response) -> None:
    """Проверка ответа при пустом списке ингредиентов"""
    check_status_code(response, 400)
    body = response.json()
    assert body['success'] is False
    assert body['message'] == config.MSG_INGREDIENTS_REQUIRED


@allure.step('Проверить ошибку: неверный hash ингредиентов')
def check_invalid_ingredient_hash_error(response: requests.Response) -> None:
    """Проверка ответа при невалидном хеше ингредиента"""
    check_status_code(response, 500)
