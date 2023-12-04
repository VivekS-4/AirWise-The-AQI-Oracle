#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller


# In[13]:


df=pd.read_csv("Downloads//data.csv")
df


# # EDA

# In[14]:




# Correcting the 'Date' column name and setting it as the index
df['Date '] = pd.to_datetime(df['Date '])
df.set_index('Date ', inplace=True)

# Display Summary Statistics for each pollutant
print(df.describe())

# Time Series Plot for a select few pollutants
# Replace 'SO2-H01', 'SO2-H02', etc., with the pollutants you're interested in
plt.figure(figsize=(12, 6))
plt.plot(df['SO2-H01'], label='SO2-H01')
plt.plot(df['SO2-H02'], label='SO2-H02')
plt.title('Pollutants Over Time')
plt.xlabel('Date')
plt.ylabel('Concentration')
plt.legend()
plt.show()

# Seasonality Analysis - Monthly for a sp ecific pollutant
df['Month'] = df.index.month
monthly_pollutant = df.groupby('Month')['SO2-H01'].mean()
plt.figure(figsize=(10, 5))
sns.barplot(x=monthly_pollutant.index, y=monthly_pollutant.values)
plt.title('Average Monthly Concentration of SO2-H01')
plt.xlabel('Month')
plt.ylabel('Average Concentration')
plt.show()

# Correlation Analysis
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()


# # Calculating Hourly Sub index of each pollutant

# In[15]:



# Define the function to calculate PM2.5 sub-index
def get_PM25_subindex(pi):
    if pi <= 30:
        return pi * 50 / 30
    elif pi <= 60:
        return 50 + (pi - 30) * 50 / 30
    elif pi <= 90:
        return 100 + (pi - 60) * 100 / 30
    elif pi <= 120:
        return 200 + (pi - 90) * 100 / 30
    elif pi <= 250:
        return 300 + (pi - 120) * 100 / 130
    elif pi > 250:
        return 400 + (pi - 250) * 100 / 130
    else:
        return pi

# Apply the function to each hourly PM2.5 column
for hour in range(1, 25):  # For hours 1 through 24
    pm25_col = f'PM2.5-H{hour:02d}'  # PM2.5 column for the hour
    pmi_col = f'PMI-H{hour:02d}'    # New column for the PMI of the hour
    df[pmi_col] = df[pm25_col].apply(get_PM25_subindex)

df


# In[16]:


## O3 Sub-Index calculation
def get_O3_subindex(oi):
    if oi <= 50:
        return oi * 50 / 50
    elif oi <= 100:
        return 50 + (oi - 50) * 50 / 50
    elif oi <= 168:
        return 100 + (oi - 100) * 100 / 68
    elif oi <= 208:
        return 200 + (oi - 168) * 100 /40
    elif oi <= 748:
        return 300 + (oi - 208) * 100 / 539
    elif oi > 748:
        return 400 + (oi - 400) * 100 / 539
    else:
        return oi

# Apply the function to each hourly O3 column
for hour in range(1, 25):
    o3_col = f'O3-H{hour:02d}'
    o3i_col = f'O3I-H{hour:02d}'  # Updated column name for O3 sub-index
    df[o3i_col] = df[o3_col].apply(get_O3_subindex)

df


# In[17]:


def get_NO2_subindex(ni):
    if ni <= 40:
        return ni * 50 / 40
    elif ni <= 80:
        return 50 + (ni - 40) * 50 / 40
    elif ni <= 180:
        return 100 + (ni - 80) * 100 / 100
    elif ni <= 280:
        return 200 + (ni - 180) * 100 / 100
    elif ni <= 400:
        return 300 + (ni - 280) * 100 / 120
    elif ni > 400:
        return 400 + (ni - 400) * 100 / 120
    else:
        return ni# Apply the function to each hourly NO2 column

for hour in range(1, 25):
    no2_col = f'NO2-H{hour:02d}'
    ni_col = f'NI-H{hour:02d}'  # Updated column name for NO2 sub-index
    df[ni_col] = df[no2_col].apply(get_NO2_subindex)
df


# In[18]:


def get_SO2_subindex(si):
    if si <= 40:
        return si * 50 / 40
    elif si <= 80:
        return 50 + (si - 40) * 50 / 40
    elif si <= 380:
        return 100 + (si - 80) * 100 / 300
    elif si <= 800:
        return 200 + (si - 380) * 100 / 420
    elif si <= 1600:
        return 300 + (si - 800) * 100 / 800
    elif si > 1600:
        return 400 + (si - 1600) * 100 / 800
    else:
        return si
    # Apply the function to each hourly SO2 column
for hour in range(1, 25):
    so2_col = f'SO2-H{hour:02d}'
    si_col = f'SI-H{hour:02d}'  # Updated column name for SO2 sub-index
    df[si_col] = df[so2_col].apply(get_SO2_subindex)
df


# In[19]:


# Apply the function to each hourly CO column
def get_CO_subindex(ci):
    if ci <= 1:
        return ci * 50 / 1
    elif ci <= 2:
        return 50 + (ci - 1) * 50 / 1
    elif ci <= 10:
        return 100 + (ci - 2) * 100 / 8
    elif ci <= 17:
        return 200 + (ci - 10) * 100 / 7
    elif ci <= 34:
        return 300 + (ci - 17) * 100 / 17
    elif ci > 34:
        return 400 + (ci - 34) * 100 / 17
    else:
        return 0
for hour in range(1, 25):
    co_col = f'CO-H{hour:02d}'
    ci_col = f'CI-H{hour:02d}'  # Updated column name for CO sub-index
    df[ci_col] = df[co_col].apply(get_CO_subindex)
df


# # Hourly AQI Generattion

# In[20]:


# Function to calculate AQI from the sub-indices
def calculate_hourly_aqi(row):
    # Extracting the sub-indices for each pollutant for a specific hour
    hourly_aqi_values = [row[f'CI-H{hour:02d}'], row[f'SI-H{hour:02d}'], 
                         row[f'NI-H{hour:02d}'], row[f'O3I-H{hour:02d}'], 
                         row[f'PMI-H{hour:02d}']]
    # The AQI is the maximum of these sub-indices
    return max(hourly_aqi_values)

# Calculate AQI for each hour and store in new columns
for hour in range(1, 25):
    aqi_col = f'AQI-H{hour:02d}'
    df[aqi_col] = df.apply(calculate_hourly_aqi, axis=1)

# Now 'df' contains the AQI for each hour
df


# # Overall AQI

# In[21]:


# Calculate the average of the hourly AQI values
hourly_aqi_columns = [f'AQI-H{hour:02d}' for hour in range(1, 25)]
df['Overall_AQI_Avg'] = df[hourly_aqi_columns].mean(axis=1)
df


# In[24]:


def ad_fuller(timeseries):
    print('Dickey-Fuller Test indicates:')
    df_test = adfuller(timeseries, regression='ct', autolag='AIC')
    output = pd.Series(df_test[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    print(output)

# Function for SARIMA Forecast with Accuracy Metrics
def sarima_forecast_with_accuracy(df, Overall_AQI_Avg, start_date='2022-01-01', test_size=0.4, forecast_period=365):
    # Convert the index to datetime
    df.index = pd.to_datetime(df.index)

    # Split the data into training and testing sets
    train_size = int(len(df) * (1 - test_size))
    train, test = df.iloc[:train_size], df.iloc[train_size:]

    # Iterate through each target column for forecasting
    for Overall_AQI_Avg in Overall_AQI_Avg:
        print(f"\nForecasting for {Overall_AQI_Avg}")

        # Benchmark with Linear Regression
        regression = LinearRegression().fit(train.index.month.values.reshape(-1, 1), train[Overall_AQI_Avg])
        linear_pred = regression.predict(test.index.month.values.reshape(-1, 1))
        print("Linear Regression Mean squared error: %.3f" % mean_squared_error(test[Overall_AQI_Avg], linear_pred))
        print("Linear Regression Coefficient of determination: %.3f" % r2_score(test[Overall_AQI_Avg], linear_pred))

        # SARIMA model for the target column
        model = SARIMAX(train[Overall_AQI_Avg], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
                        enforce_stationarity=False, enforce_invertibility=False)
        results = model.fit(disp=False)

        # Forecast future values
        forecast_index = pd.date_range(start=test.index.min(), periods=forecast_period, freq='D')
        forecast = results.get_forecast(steps=forecast_period, index=forecast_index)

        # Evaluate model performance on the test set
        predictions = results.get_prediction(start=test.index.min(), end=test.index.max(), dynamic=False)
        mse = ((predictions.predicted_mean - test[Overall_AQI_Avg]) ** 2).mean()

        # Print Mean Squared Error (MSE) as a measure of model performance
        print(f'SARIMA Mean Squared Error (MSE) for {Overall_AQI_Avg}: {mse:.2f}')

        # R-squared (coefficient of determination) as a measure of explained variance
        r2 = r2_score(test[Overall_AQI_Avg], predictions.predicted_mean)
        print(f'R-squared for {Overall_AQI_Avg}: {r2:.3f}')

        # Plot original data, testing data, and forecasted values
        plt.figure(figsize=(12, 6))
        plt.plot(train.index, train[Overall_AQI_Avg], label='Training Data')
        plt.plot(test.index, test[Overall_AQI_Avg], label='Testing Data', color='blue')
        plt.plot(forecast_index, forecast.predicted_mean, label=f'SARIMA Forecasted Values ({Overall_AQI_Avg})', color='red')
        plt.plot(test.index, linear_pred, label=f'Linear Regression Benchmark ({Overall_AQI_Avg})', color='green')
        plt.title(f'SARIMA Forecast vs. Linear Regression Benchmark ({Overall_AQI_Avg})')
        plt.xlabel('Date')
        plt.ylabel(Overall_AQI_Avg)
        plt.legend()
        plt.show()

        # Residual Analysis
        residuals = test[Overall_AQI_Avg] - predictions.predicted_mean
        residuals.plot(label='Residuals', color='green')
        plt.axhline(0, color='black', linestyle='--', linewidth=1, label='Zero Line (Mean Residuals)')
        plt.title(f'Residual Analysis ({Overall_AQI_Avg})')
        plt.xlabel('Date')
        plt.ylabel('Residuals')
        plt.legend()
        plt.show()

# Apply the SARIMA forecast function with accuracy metrics
sarima_forecast_with_accuracy(df, Overall_AQI_Avg)


# In[ ]:




