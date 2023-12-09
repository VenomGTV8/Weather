from datetime import datetime, timedelta, timezone


class SelectionNecDataException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def selection_necessary_data(data_from_api: dict) -> dict:
    """происходит отбор нужных для вывода данных"""
    try:
        time_and_date = datetime.fromtimestamp(
            data_from_api.get("dt"),
            timezone(timedelta(seconds=data_from_api.get("timezone"))),
        )
        necessary_data = {
            "current_time": str(time_and_date),
            "city_name": str(data_from_api["name"]),
            "weather": str(data_from_api["weather"][0]["description"]),
            "temp_cur": data_from_api["main"]["temp"],
            "temp_feels": data_from_api["main"]["feels_like"],
            "wind_speed": data_from_api["wind"]["speed"],
        }
        return necessary_data
    except Exception:
        raise SelectionNecDataException(
            "Произошла ошибка при обработке данных, полученных с сервера."
        )
