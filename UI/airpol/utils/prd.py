import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from keras.layers import InputLayer, LSTM, Dense
from keras.models import Sequential


model = Sequential()
model.add(InputLayer(input_shape=(24, 24)))  # Define the input shape explicitly
model.add(LSTM(units=50, activation='relu'))  # Add other layers as needed
model.add(Dense(units=1, activation='linear'))  # Add other layers as needed

# Compile the model
model.compile(optimizer='adam', loss='mae', metrics=['accuracy'])

# Now save the model
model.save('m.keras')

# Load your dataset
df = pd.read_csv("D:/temp/UI/airpol/utils/weather.csv")
df = df.dropna()
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
df = df.drop(['date', 'time'], axis=1)
df = df.drop(columns=['Document ID'])
df['longitude'] = df['longitude'].astype('float64')
df['latitude'] = df['latitude'].astype('float64')
df = pd.get_dummies(df, columns=df.select_dtypes(include=['object']).columns, drop_first=True)
# Create lag features for all air quality metrics using .loc
df.loc[:, 'pm2_5_lag1'] = df['pm2_5'].shift(1)
df.loc[:, 'pm10_lag1'] = df['pm10'].shift(1)
df.loc[:, 'o3_lag1'] = df['o3'].shift(1)
df.loc[:, 'co_lag1'] = df['co'].shift(1)
df.loc[:, 'no2_lag1'] = df['no2'].shift(1)
df.loc[:, 'so2_lag1'] = df['so2'].shift(1)
df.loc[:, 'gb_defra_index_lag1'] = df['gb_defra_index'].shift(1)
df.loc[:, 'us_epa_index_lag1'] = df['us_epa_index'].shift(1)
df = df.sort_values(by='datetime')

def predict_for_city(city_name, model_filename="m.keras"):
    # List of pollutants to predict
    pollutants = ['so2', 'no2', 'CO', 'pm3_5', 'o3'] 

    # Placeholder for predictions
    predictions = {}

    for target_pollutant in pollutants:
        # Extract the relevant columns for the LSTM model (include all 24 hours for the specified pollutant)
        columns_to_use = ['name', 'datetime'] + [f'{target_pollutant}']
        data = df[columns_to_use]

        # Filter data for the specified city
        data_city = data[data['name'] == city_name]

        # Convert the 'Date' column to datetime and set it as the index
        data_city.loc[:, 'datetime'] = pd.to_datetime(data_city['datetime'], format='mixed')

        # Extract only numeric columns for scaling
        numeric_columns = data_city.select_dtypes(include=np.number).columns
        data_numeric = data_city[numeric_columns]

        # Normalize the data using Min-Max scaling
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data_numeric)

        # Create sequences for predicting with the LSTM model
        sequence_length = 24  # Assuming you want to use the last 24 hours to predict the next measurement
        last_sequence = data_scaled[-sequence_length:].reshape(1, sequence_length, len(numeric_columns))

        # Load the pre-trained model
        model = load_model(model_filename)

        # Predict the next measurement for a given sequence
        predicted_scaled = model.predict(last_sequence)

        # Inverse transform the predicted value to get the actual measurement
        last_sequence_reshaped = last_sequence[0][-1][:-1].reshape(1, -1)  # Reshape to a 2D array
        predicted_measurement = scaler.inverse_transform(
            np.concatenate([last_sequence_reshaped, predicted_scaled], axis=1))

        # Store the prediction
        predictions[target_pollutant] = predicted_measurement[0][-1]

    return predictions

# Replace "YourCityName" with the actual city name you want to predict
city_name = "oshawa"



# Ensure the entered city name is in title case (e.g., "New York" instead of "new york")
city_name = city_name.title()

# Call the predict_for_city function with the pre-trained model
city_predictions = predict_for_city(city_name, model_filename="m.keras")

# Print predictions for each pollutant
for pollutant, prediction in city_predictions.items():
    print(f"Predicted {pollutant} for the next hour in {city_name}: {prediction}")

# Determine the overall AQI
overall_aqi = max(city_predictions.values())

# Output overall AQI
print(f"\nOverall predicted AQI: {overall_aqi}")