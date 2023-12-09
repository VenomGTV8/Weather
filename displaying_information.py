from settings import WEATHER_TEXT


def print_history(data_from_file: list):
    count_weather_data = input("\nСколько последних записей вы хотите увидеть? ")

    if count_weather_data.isdigit():
        count_weather_data = int(count_weather_data)
        if count_weather_data == 0:
            print("Истории запросов пока что нет.")
        elif count_weather_data >= len(data_from_file):
            for record in data_from_file:
                output_data_weather(record)
        else:
            for record in data_from_file[:count_weather_data]:
                output_data_weather(record)
    else:
        print("Вы ввели некорректое значение. Попробуйте ввести положительное число.")


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
