from datetime import datetime, timedelta, timezone
import json
import requests
import geocoder

API_KEY = "596a4997d72919d958e0532e4543d0da"
API_URL = (
    "http://api.openweathermap.org/data/2.5/weather?"
    "q={}&units=metric&appid={}&lang=ru"
)

MENU_TEXT = (
    "\n1. Погода по текущему местоположению\n2. Погода по названию города\n"
    "3. Просмотр истории запросов\n4. Очистить историю запросов\n\n0. Закрыть программу\n"
)

WEATHER_TEXT = (
    "\nТекущее время: {date_time}\n"
    "Название города: {city_name}\n"
    "Погодные условия: {weather}\n"
    "Текущая температура: {temp_cur}\n"
    "Ощущается как: {temp_feels}\n"
    "Скорость ветра: {wind_speed}\n"
)
FILENAME_HISTORY = "data.json"


class SaveToJsonException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class GeocoderException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class SelectionNecDataException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def delete_history():
    try:
        with open(FILENAME_HISTORY, "w") as file:
            file.write(json.dumps([], indent=4, ensure_ascii=False))
            print("\nИстория прогноза погоды удалена.")
    except Exception:
        raise SaveToJsonException(
            "Проблема с удалением данных. Приносим свои извинения."
        )


def create_file_json():
    data_from_file = []
    with open(FILENAME_HISTORY, "w") as file:
        json.dump(data_from_file, file)


def read_json():
    try:
        with open(FILENAME_HISTORY, "r+") as file:
            data_from_file = json.load(file)
        return data_from_file
    except FileNotFoundError:
        create_file_json()
    except Exception:
        raise SaveToJsonException("Проблемы с чтением данных. Приносим свои извинения.")


def write_to_json(data: dict) -> None:
    list_to_json = read_json()
    try:
        with open(FILENAME_HISTORY, "w+") as file:
            if list_to_json is None or list_to_json == "":
                list_to_json = []
            list_to_json.append(data)
            json.dump(
                list_to_json,
                file,
                indent=4,
                ensure_ascii=True,
            )
    except Exception:
        raise SaveToJsonException(
            "Проблемы с сохранением в базу данных. Приносим свои извинения."
        )


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


def output_data_weather(necessary_data: dict):
    """Функция выводит пользователю инфу в консоли в нужном формате"""
    print(
        WEATHER_TEXT.format(
            date_time=necessary_data.get("current_time"),
            city_name=necessary_data.get("city_name"),
            weather=necessary_data.get("weather"),
            temp_cur=necessary_data.get("temp_cur"),
            temp_feels=necessary_data.get("temp_feels"),
            wind_speed=necessary_data.get("wind_speed"),
        )
    )


def data_manipulation(data_from_api: dict):
    """Получил словарь со множеством данных. Надо взять только нужные - одна новая функция.
    Вернутся нужные данные. Их нужно вывести в определенном формате - вторая функция.
    Сохраняем данные? Да. Третья функция.
    Начнем
    """
    necessary_data = selection_necessary_data(data_from_api)
    output_data_weather(necessary_data)
    write_to_json(necessary_data)


def get_current_location():
    """Поулчаем название города текущего местоположения"""
    try:
        return geocoder.ip("me").city
    except Exception:
        raise GeocoderException(
            "Не удалось определить текущее местоположение. Попробуйте позже."
        )


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


def main():
    while True:
        print(MENU_TEXT)
        user_input = input("\nВыберите действие: ").strip()

        try:
            if user_input == "0":
                break
            elif user_input == "1":
                city_name = get_current_location()
                response = get_information_from_api(city_name)
                data_manipulation(response)
            elif user_input == "2":
                city_name = input("\nПожалуйста, введите название города: ").strip()
                response = get_information_from_api(city_name)
                data_manipulation(response)
            elif user_input == "3":
                pass
            elif user_input == "4":
                delete_history()
            else:
                raise ValueError
        except requests.exceptions.HTTPError:
            print("Данного города не существует. Попробуйте другой.")
        except requests.exceptions.RequestException:
            print("Проблемы с соединением. попрообуйте позже.")
        except GeocoderException as exp:
            print(exp)
        except SelectionNecDataException as exp:
            print(exp)
        except SaveToJsonException as exp:
            print(exp)
        except FileNotFoundError:
            print("Произошла ошибка при сохранении запроса.")
        except ValueError:
            print("Данного действия нет! Давай по новой.")
        except Exception:
            print("Произошла непредвиденная ошибка. Попробуйте позже.")


if __name__ == "__main__":
    main()
