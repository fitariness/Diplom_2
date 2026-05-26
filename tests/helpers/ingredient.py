from api.stellar_burgers_api import StellarBurgersApi


def get_ingredient_ids(api: StellarBurgersApi, count: int = 2) -> list[str]:
    response = api.get_ingredients()
    return [item['_id'] for item in response.json()['data'][:count]]
