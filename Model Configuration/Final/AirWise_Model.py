#!/usr/bin/env python
# coding: utf-8

# # Loading Necessary Libraries

# In[4]:


import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense


# # Loading Dataset

# In[5]:


# Load your dataset
df = pd.read_csv("cleaned_data.csv")
df


# # AQI predictions

# In[6]:


def predict_aqi_for_city(city_name):
    # List of pollutants to predict
    pollutants = ['SO2', 'NO2', 'CO', 'PM2.5', 'O3']  
    predictions = {}

    for target_pollutant in pollutants:
        # Extract the relevant columns for the LSTM model
        columns_to_use = ['City', 'Date'] + [f'{target_pollutant}-H{i}' for i in range(1, 25)]
        data = df[columns_to_use]

        # Filter data for the specified city
        data_city = data[data['City'] == city_name]

        # Convert the 'Date' column to datetime and set it as the index
        data_city = data_city.copy()
        data_city.loc[:, 'Date'] = pd.to_datetime(data_city['Date'])

        # Extract only numeric columns for scaling
        numeric_columns = data_city.select_dtypes(include=np.number).columns
        data_numeric = data_city[numeric_columns]

        # Normalizing the data using Min-Max scaling
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data_numeric)

        # Creating sequences for training the LSTM model
        sequence_length = 24  # Assuming you want to use the last 24 hours to predict the next measurement
        X, y = [], []

        for i in range(len(data_scaled) - sequence_length):
            X.append(data_scaled[i:i + sequence_length])
            y.append(data_scaled[i + sequence_length])

        X = np.array(X)
        y = np.array(y)

        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Building the LSTM model
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
        last_sequence_reshaped = last_sequence[0][-1][:-1].reshape(1, -1)  # Reshape to a 2D array
        predicted_measurement = scaler.inverse_transform(
            np.concatenate([last_sequence_reshaped, predicted_scaled], axis=1))

        # Store the prediction
        predictions[target_pollutant] = predicted_measurement[0][-1]

    return predictions


# In[7]:


# taking input of city
city_name = input("Enter the city name: ")
city_name = city_name.title()

# Calling the predict_aqi_for_city function with the user-inputted city name
city_predictions = predict_aqi_for_city(city_name)

# Print predictions for each pollutant
for pollutant, prediction in city_predictions.items():
    print(f"Predicted {pollutant} for the next day in {city_name}: {prediction}")

# Determine the overall AQI
overall_aqi = max(city_predictions.values())

# Output overall AQI
print(f"\nOverall predicted AQI for the next day: {overall_aqi}")


# In[ ]:




