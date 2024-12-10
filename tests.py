import requests
from app import check_bad_weather

BASE_URL = "http://127.0.0.1:5000/weather_check"

def test_check_bad_weather():
    """Простой тест функции check_bad_weather."""
    assert check_bad_weather(-5, 10, 0) == "Плохие погодные условия", "Ошибка: низкая температура"
    assert check_bad_weather(40, 10, 0) == "Плохие погодные условия", "Ошибка: высокая температура"
    assert check_bad_weather(25, 60, 0) == "Плохие погодные условия", "Ошибка: сильный ветер"
    assert check_bad_weather(25, 10, 80) == "Плохие погодные условия", "Ошибка: высокая вероятность осадков"
    assert check_bad_weather(25, 10, 20) == "Хорошие погодные условия", "Ошибка: нормальные условия"

def test_weather_check():
    """Простой тест эндпоинта /weather_check."""
    payload = {"latitude": 55.7522, "longitude": 37.6156}  # Координаты Москвы
    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 200, "Ошибка: неправильный статус ответа"

    data = response.json()
    assert "weather_condition" in data, "Ошибка: отсутствует ключ 'weather_condition' в ответе"
    print(f"Условие погоды: {data['weather_condition']}")

def test_weather_check_no_data():
    response = requests.post(BASE_URL, json={})

    assert response.status_code == 400, "Ошибка: неправильный статус ответа для отсутствующих данных"

    data = response.json()
    assert "error" in data, "Ошибка: отсутствует ключ 'error' в ответе"
    print(f"Сообщение об ошибке: {data['error']}")

if __name__ == "__main__":
    # Запуск всех тестов
    print("Тестируем функцию check_bad_weather...")
    test_check_bad_weather()

    print("Тестируем эндпоинт /weather_check...")
    test_weather_check()

    print("Тестируем эндпоинт /weather_check без данных...")
    test_weather_check_no_data()

    print("Все тесты завершены успешно!")
