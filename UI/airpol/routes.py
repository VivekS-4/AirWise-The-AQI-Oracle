from flask import render_template, request, jsonify
import requests
from airpol import airpol
from airpol.utils.prediction import predict_for_city
import sqlite3

conn = sqlite3.connect('predictions.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        city TEXT,
        SO2 REAL,
        NO2 REAL,
        CO REAL,
        PM25 REAL,
        O3 REAL,
        overall_aqi REAL
    )
''')



print("Predictions saved to the database.")

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

    cursor.execute('''
    INSERT INTO predictions (city, SO2, NO2, CO, PM25, O3, overall_aqi)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (city_name, predicted_SO2, predicted_NO2, predicted_CO, predicted_PM25, predicted_O3, overall_aqi))

    conn.commit()
    conn.close()

    # Call the predict_for_city function with the user-entered city name
    
    print(f"Predicted SO2 for the next hour in {city_name}: {predicted_SO2}")
    print(f"Predicted NO2 for the next hour in {city_name}: {predicted_NO2}")
    print(f"Predicted CO for the next hour in {city_name}: {predicted_CO}")
    print(f"Predicted PM2.5 for the next hour in {city_name}: {predicted_PM25}")
    print(f"Predicted O3 for the next hour in {city_name}: {predicted_O3}")
    print(f"\nOverall predicted AQI: {overall_aqi}")


    new_predicted_SO2 = city_predictions['SO2']
    new_predicted_NO2 = city_predictions['NO2']
    new_predicted_CO = city_predictions['CO']
    new_predicted_PM25 = city_predictions['PM2.5']
    new_predicted_O3 = city_predictions['O3']
    # Determine the overall AQI
    new_overall_aqi = max(city_predictions.values())
    new_city_name = city_name

    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()

# Update values for a specific city
    cursor.execute('''
        UPDATE predictions
        SET SO2 = ?, NO2 = ?, CO = ?, PM25 = ?, O3 = ?, overall_aqi = ?
        WHERE city = ?
        ''', (new_predicted_SO2, new_predicted_NO2, new_predicted_CO, new_predicted_PM25, new_predicted_O3, new_overall_aqi, new_city_name))

    conn.commit()
    conn.close()

    print("Predictions updated in the database.")
    

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
