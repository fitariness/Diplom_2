import uuid


def unique_email() -> str:
    return f'autotest_{uuid.uuid4().hex}@yandex.ru'


def default_user_payload(email: str | None = None) -> dict:
    return {
        'email': email or unique_email(),
        'password': '123456',
        'name': 'Autotest User',
    }


def user_payload_without_field(missing_field: str) -> dict:
    payload = default_user_payload()
    del payload[missing_field]
    return payload
