from database_actions import SaveToJsonException
from data_processing import SelectionNecDataException
from database_actions import write_to_json, read_json, delete_history
from data_processing import selection_necessary_data
from get_weather_forecast import *
from displaying_information import print_history, output_data_weather
from settings import MENU_TEXT


def data_manipulation(data_from_api: dict):
    """Получил словарь со множеством данных. Надо взять только нужные - одна новая функция.
    Вернутся нужные данные. Их нужно вывести в определенном формате - вторая функция.
    Сохраняем данные? Да. Третья функция.
    Начнем
    """
    necessary_data = selection_necessary_data(data_from_api)
    output_data_weather(necessary_data)
    write_to_json(necessary_data)


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
                print_history(read_json())
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
