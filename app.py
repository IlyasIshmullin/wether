import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
API_KEY = 'HWBUjLqqgTZDVWDVbPq7OkNtkrq6dLp6'

def get_location_key(lat, lon, api_key):
    """Получает locationKey на основе широты и долготы."""
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {
        "apikey": api_key,
        "q": f"{lat},{lon}",
        "language": "ru-ru"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('Key')
    except requests.RequestException as e:
        app.logger.error(f"Ошибка при запросе к API AccuWeather (location): {e}")
        return None

def get_weather_data(location_key, api_key):
    """Получает текущие данные о погоде на основе locationKey."""
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    params = {
        "apikey": api_key,
        "language": "ru-ru",
        "details": "true"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None
    except requests.RequestException as e:
        app.logger.error(f"Ошибка при запросе к API AccuWeather (weather): {e}")
        return None

def check_bad_weather(temperature, wind_speed, rain_probability):
    """Проверяет, является ли погода плохой."""
    if (temperature < 0 or temperature > 35) or wind_speed > 50 or rain_probability > 70:
        return "Плохие погодные условия"
    return "Хорошие погодные условия"

@app.route('/weather_check', methods=['POST'])
def weather_check():
    """Обрабатывает запрос на проверку погодных условий."""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            return jsonify({"error": "Укажите 'latitude' и 'longitude' в запросе"}), 400

        location_key = get_location_key(latitude, longitude, API_KEY)
        if not location_key:
            return jsonify({"error": "Ошибка получения locationKey"}), 500

        weather_data = get_weather_data(location_key, API_KEY)
        if not weather_data:
            return jsonify({"error": "Ошибка получения данных о погоде"}), 500

        temperature = weather_data['Temperature']['Metric']['Value']
        wind_speed = weather_data['Wind']['Speed']['Metric']['Value']
        rain_probability = weather_data.get('PrecipitationSummary', {}).get('PrecipitationProbability', 0)

        weather_condition = check_bad_weather(temperature, wind_speed, rain_probability)
        return jsonify({"weather_condition": weather_condition})

    except Exception as e:
        app.logger.error(f"Непредвиденная ошибка: {e}")
        return jsonify({"error": f"Непредвиденная ошибка: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)