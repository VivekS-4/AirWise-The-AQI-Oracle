from flask import render_template, request, jsonify
import requests
from airpol import airpol
from airpol.utils.prediction import predict_for_city

api_key = '4fb39bf5c97d06c2a97e2884ecc992de'  # Replace 'YOUR_API_KEY' with your Weatherstack API key


@airpol.route('/')
def initial():
    return render_template('initial_page.html')


@airpol.route('/index')
def index():
    return render_template('index.html')


@airpol.route('/predict', methods=['POST'])
def predict():
    city_name = request.form.get('city')
    city_name = city_name.title()  # Capitalize the city name
    
    city_predictions = predict_for_city(city_name, model_filename="m.keras")

    # Initialize variables to store predicted values
    predicted_SO2 = city_predictions['SO2']
    predicted_NO2 = city_predictions['NO2']
    predicted_CO = city_predictions['CO']
    predicted_PM25 = city_predictions['PM2.5']
    predicted_O3 = city_predictions['O3']
    # Determine the overall AQI
    overall_aqi = max(city_predictions.values())

    # Call the predict_for_city function with the user-entered city name
    
    print(f"Predicted SO2 for the next hour in {city_name}: {predicted_SO2}")
    print(f"Predicted NO2 for the next hour in {city_name}: {predicted_NO2}")
    print(f"Predicted CO for the next hour in {city_name}: {predicted_CO}")
    print(f"Predicted PM2.5 for the next hour in {city_name}: {predicted_PM25}")
    print(f"Predicted O3 for the next hour in {city_name}: {predicted_O3}")
    print(f"\nOverall predicted AQI: {overall_aqi}")

    

    return "Predictions saved to local variables."


@airpol.route('/get_temperature', methods=['POST'])
def get_temperature():
    city = request.json.get('city')

    # Extracting only the first word of the city name
    first_word = city.split()[0]

    # API call to fetch weather data
    weather_url = f'http://api.weatherstack.com/current?access_key={api_key}&query={first_word}'
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temperature']
        return jsonify({'temperature': temperature})
    else:
        return jsonify({'error': 'City not found. Please try again.'}), 404
