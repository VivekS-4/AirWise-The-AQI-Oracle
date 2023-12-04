import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


warnings.filterwarnings("ignore")

# Load your dataset
df = pd.read_csv("D:/temp/UI/airpol/utils/data.csv")

# Remove extra whitespaces in column names
df.columns = df.columns.str.strip()


def predict_for_city(city_name):
    # List of pollutants to predict
    pollutants = ['SO2', 'NO2', 'CO', 'PM2.5', 'O3']  # Replace with actual pollutants

    # Placeholder for predictions
    predictions = {}

    for target_pollutant in pollutants:
        # Extract the relevant columns for the LSTM model
        # Generate columns to use
        target_columns = [f'{target_pollutant}-H{i:02d}' for i in range(1, 25)]
        columns_to_use = ['City', 'Date'] + target_columns

        # Check if all columns in columns_to_use are present in the DataFrame
        if not all(col in df.columns for col in columns_to_use):
            print(f"Columns {target_columns} do not exist for {target_pollutant}. Skipping...")
            continue
        data = df[columns_to_use]

        # Filter data for the specified city
        data_city = data[data['City'] == city_name]

        # Convert the 'Date' column to datetime and set it as the index
        data_city['Date'] = pd.to_datetime(data_city['Date'])

        # Extract only numeric columns for scaling
        numeric_columns = data_city.select_dtypes(include=np.number).columns
        data_numeric = data_city[numeric_columns]

        # Normalize the data using Min-Max scaling
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data_numeric)

        # Create sequences for training the LSTM model
        sequence_length = 24
        X, y = [], []

        for i in range(len(data_scaled) - sequence_length):
            X.append(data_scaled[i:i + sequence_length])
            y.append(data_scaled[i + sequence_length])

        X = np.array(X)
        y = np.array(y)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Build the LSTM model
        model = Sequential()
        model.add(LSTM(units=50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
        model.add(Dense(units=1))

        model.compile(optimizer='adam', loss='mae')

        # Train the model
        model.fit(X_train, y_train, epochs=50, verbose=0, batch_size=32, validation_data=(X_test, y_test))

        # Predict the next measurement for a given sequence
        last_sequence = X[-1].reshape(1, sequence_length, len(numeric_columns))
        predicted_scaled = model.predict(last_sequence)

        # Inverse transform the predicted value to get the actual measurement
        last_sequence_reshaped = last_sequence[0][-1][:-1].reshape(1, -1)
        predicted_measurement = \
            (scaler.inverse_transform(np.concatenate([last_sequence_reshaped, predicted_scaled], axis=1)))

        # Store the prediction
        predictions[target_pollutant] = predicted_measurement[0][-1]

    return predictions

# city_name = input("Enter the city name: ")
# city_name = city_name.title()
# city_predictions = predict_for_city(city_name)
# for pollutant, prediction in city_predictions.items():
#     print(f"Predicted {pollutant} for the next hour in {city_name}: {prediction}")
#
#
# overall_aqi = max(city_predictions.values())
#
# print(f"\nOverall predicted AQI: {overall_aqi}")