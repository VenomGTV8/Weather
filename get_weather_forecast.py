import requests
import geocoder
from settings import API_KEY, API_URL


class GeocoderException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def get_information_from_api(city_name: str):
    """Получаем данные о погоде с апихи"""
    try:
        response = requests.get(API_URL.format(city_name, API_KEY), timeout=3)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException


def get_current_location():
    """Поулчаем название города текущего местоположения"""
    try:
        return geocoder.ip("me").city
    except Exception:
        raise GeocoderException(
            "Не удалось определить текущее местоположение. Попробуйте позже."
        )
