import csv
from flask import render_template, request, jsonify, send_file
from airpol import airpol
from airpol.utils.prediction import predict_for_city
import requests

print("Predictions saved to the CSV file.")

def clear_csv_file():
    with open('predictions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['City', 'SO2', 'NO2', 'CO', 'PM25', 'O3', 'Overall AQI'])
    print("CSV file cleared successfully.")

@airpol.route('/get_csv_data')
def get_csv_data():
    # Read the CSV file and send it as a response
    try:
        with open('D:/temp/UI/predictions.csv', 'r') as file:
            csv_data = file.read()
            return csv_data, 200, {'Content-Type': 'text/csv'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@airpol.route('/')
def initial():
    return render_template('initial_page.html')

@airpol.route('/index')
def index():
    with open('predictions.csv', newline='') as file:
        reader = csv.reader(file)
        data = next(reader)

    return render_template('index.html', prediction_data=data)

@airpol.route('/predict', methods=['POST'])
def predict():
    clear_csv_file()

    city_name = request.form.get('city')
    if not city_name:
        return "No city provided"

    city_name = city_name.title()

    city_predictions = predict_for_city(city_name, model_filename="m.keras")

    predicted_SO2 = city_predictions['SO2']
    predicted_NO2 = city_predictions['NO2']
    predicted_CO = city_predictions['CO']
    predicted_PM25 = city_predictions['PM2.5']
    predicted_O3 = city_predictions['O3']
    overall_aqi = max(city_predictions.values())

    with open('predictions.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([city_name, predicted_SO2, predicted_NO2, predicted_CO, predicted_PM25, predicted_O3, overall_aqi])

    print("Predictions saved in the CSV file.")

    return jsonify({
        'success': True,  # Optionally, include additional response data
        'message': 'Data fetched successfully'  # Example message
    })

@airpol.route('/get_temperature', methods=['POST'])
def get_temperature():
    city = request.json.get('city')

    first_word = city.split()[0]

    api_key = '4fb39bf5c97d06c2a97e2884ecc992de'
    weather_url = f'http://api.weatherstack.com/current?access_key={api_key}&query={first_word}'
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temperature']
        return jsonify({'temperature': temperature})
    else:
        return jsonify({'error': 'City not found. Please try again.'}), 404

import requests
from flask import jsonify

@airpol.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.json.get('city')

    first_word = city.split()[0]

    api_key = '10048207c054999ff6ea2188e2c65579'
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={first_word}&appid={api_key}&units=metric'

    response = requests.get(weather_url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        weather = {
            'temperature': temperature,
            'description': description
        }
        return jsonify(weather)
    else:
        return jsonify({'error': 'City not found. Please try again.'}), 404

@airpol.route('/how')
def how():
    return render_template('index.html')
@airpol.route('/why')
def why():
    return render_template('why.html')