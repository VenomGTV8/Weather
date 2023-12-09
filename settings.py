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


API_KEY = "596a4997d72919d958e0532e4543d0da"
API_URL = (
    "http://api.openweathermap.org/data/2.5/weather?"
    "q={}&units=metric&appid={}&lang=ru"
)
