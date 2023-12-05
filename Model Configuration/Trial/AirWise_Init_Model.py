#!/usr/bin/env python
# coding: utf-8

# # Importing necessary libraries

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score
from sklearn.model_selection import GridSearchCV
import seaborn as sns


# # Loading the data

# In[2]:


data = pd.read_csv('downloads//data.csv')
data


# ### Checking for null values

# In[3]:


#looking for null values in every column
data.isnull().sum()


# ### Visually represents null values

# In[4]:


# Shows if there are any null values (yellow part represents null values)
sns.heatmap(data.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# # Handling Outliers

# In[5]:


def handle_outliers(data, column_name):

    # Calculate Q1, Q2 and IQR
    Q1 = data[column_name].quantile(0.25)
    Q3 = data[column_name].quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Handle outliers
    data[column_name] = data[column_name].apply(lambda x: lower_bound if x < lower_bound else x)
    data[column_name] = data[column_name].apply(lambda x: upper_bound if x > upper_bound else x)
    
    return data


# In[6]:


columns_to_check = ["PM25","SO2", "NO2", "CO", "O3"]

for col in columns_to_check:
    data[col] = pd.to_numeric(data[col], errors='coerce')


# In[7]:


columns_to_check = ["PM25","SO2", "NO2", "CO", "O3"]

for col in columns_to_check:
    data = handle_outliers(data, col)


# In[8]:


from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
data['city_encoded'] = encoder.fit_transform(data['City'])
data.drop('City', axis=1, inplace=True)


# In[9]:


data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)



# In[10]:


# Fill missing values - for simplicity, using mean
data.fillna(data.mean(), inplace=True)

# Standardize data
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)


# In[11]:


data.isnull().sum()


# In[12]:


# for col in columns_to_check:
#     data[col].fillna(data[col].median(), inplace=True)


# In[13]:


data.isnull().sum()


# In[14]:


sns.heatmap(data.isnull(),yticklabels=False,cbar=False,cmap='viridis')


# # Representing Skewness of each pollutant

# In[15]:


first_five_columns = data.iloc[:, :5]
first_five_columns.hist(bins=50, figsize=(20, 15))

# Show the plot
plt.show()


# # Calculating Sub Index of each pollutant

# In[16]:


## PM2.5 Sub-Index calculation
def get_PM25_subindex(pi):
    if pi <= 30:
        return pi * 50 / 30
    elif pi <= 60:
        return 50 + (pi- 30) * 50 / 30
    elif pi <= 90:
        return 100 + (pi- 60) * 100 / 30
    elif pi <= 120:
        return 200 + (pi- 90) * 100 / 30
    elif pi <= 250:
        return 300 + (pi- 120) * 100 / 130
    elif pi > 250:
        return 400 + (pi- 250) * 100 / 130
    else:
        return pi
data['PMI']=data['PM25'].apply(get_PM25_subindex)
data[['PM25','PMI']].reset_index(drop=True)



# In[17]:


## O3 Sub-Index calculation
def get_O3_subindex(oi):
    if oi <= 50:
        return oi * 50 / 50
    elif oi <= 100:
        return 50 + (oi - 50) * 50 / 50
    elif oi <= 168:
        return 100 + (oi - 100) * 100 / 68
    elif oi <= 208:
        return 200 + (oi - 168) * 100 / 40
    elif oi <= 748:
        return 300 + (oi - 208) * 100 / 539
    elif oi > 748:
        return 400 + (oi - 400) * 100 / 539
    else:
        return oi
data['O3I']=data['O3'].apply(get_O3_subindex)
data[['O3','O3I']].reset_index(drop=True)


# In[18]:


## NOx Sub-Index calculation
def get_NOx_subindex(ni):
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
        return ni
data['NOI']=data['NO2'].apply(get_NOx_subindex)
data[['NO2','NOI']].reset_index(drop=True)


# In[19]:


## SO2 Sub-Index calculation
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
data['SOI']=data['SO2'].apply(get_SO2_subindex)
data[['SO2', 'SOI']].reset_index(drop=True)


# In[20]:


## CO Sub-Index calculation
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
data['COI']=data['CO'].apply(get_CO_subindex)
data[['CO','COI']].reset_index(drop=True)



# # Calculating Air Quality Index

# In[21]:


def cal_aqi(pi,oi,ni,si,ci):
    aqi=0
    if(pi>oi and pi>ni and pi>si and pi>ci):
        aqi=pi
    if(oi>pi and oi>ni and oi>si and oi>ci):
        aqi=oi
    if(ni>pi and ni>oi and ni>si and ni>ci):
        aqi=ni
    if(si>pi and si>oi and si>ni and si>ci):
        aqi=si
    if(ci>pi and ci>oi and ci>ni and ci>si):
        aqi=ci
    return aqi

data['AQI'] = data.apply(lambda x:cal_aqi(x['PMI'],x['O3I'],x['NOI'],x['SOI'],x['COI']),axis=1)
data[['PMI','O3I','NOI','SOI','COI','AQI']]


# In[22]:


def get_AQI_Range(x):
    if x <= 50:
        return "Good"
    elif x <= 100:
        return "Satisfactory"
    elif x <= 200:
        return "Moderate"
    elif x <= 300:
        return "Poor"
    elif x <= 400:
        return "Very Poor"
    elif x > 400:
        return "Severe"
    else:
        return np.NaN

data['AQI_Range'] = data['AQI'].apply(get_AQI_Range)
data


# In[23]:


data['AQI_Range'].value_counts()


# # Setting up dependent and independent variables

# In[24]:


X=data[['PMI','O3I','SOI','COI']]
y=data[['AQI']]
X.head()


# In[25]:


y.head()


# # Decision Tree Regressor

# In[26]:


# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train.shape,X_test.shape,y_train.shape,y_test.shape)


# In[27]:


dt=DecisionTreeRegressor()
dt.fit(X_train,y_train)


# In[28]:


train_prdt=dt.predict(X_train)
test_prdt=dt.predict(X_test)


# In[29]:


RMSE_train=(np.sqrt(mean_squared_error(y_train,train_prdt)))
RMSE_test=(np.sqrt(mean_squared_error(y_test,test_prdt)))
print("RMSE Training Data = ",str(RMSE_train))
print("RMSE Testing Data = ",str(RMSE_test))
print("-"*50)

print("RSquared Training Data = ",dt.score(X_train,y_train)) 
print("RSquared Testing Data = ",dt.score(X_test,y_test)) 


# # Random Forest Regressor

# In[30]:


rf=RandomForestRegressor().fit(X_train,y_train)


# In[31]:


train_prdt1=rf.predict(X_train)
test_prdt1=rf.predict(X_test)


# In[32]:


RMSE_train1=(np.sqrt(mean_squared_error(y_train,train_prdt1)))
RMSE_test1=(np.sqrt(mean_squared_error(y_test,test_prdt1)))
print("RMSE Training Data = ",str(RMSE_train1))
print("RMSE Testing Data = ",str(RMSE_test1))
print("-"*50)

print("RSquared Training Data = ",rf.score(X_train,y_train)) 
print("RSquared Testing Data = ",rf.score(X_test,y_test))  


# # HyperParameter Tuning on Decision tree

# In[33]:


# Define the Decision Tree model
dt = DecisionTreeRegressor(random_state=42)

# Define the parameter grid for the Decision Tree
param_grid_dt = {
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2', None]
}

# Set up Grid Search with cross-validation for Decision Tree
grid_search_dt = GridSearchCV(estimator=dt, param_grid=param_grid_dt, cv=5, n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

# Fit the grid search to the data
grid_search_dt.fit(X_train, y_train)

# Best parameters found for Decision Tree
best_parameters_dt = grid_search_dt.best_params_
print("Best Parameters for Decision Tree: ", best_parameters_dt)

#Use these parameters to train final Decision Tree model
final_model_dt = DecisionTreeRegressor(**best_parameters_dt)
final_model_dt.fit(X_train, y_train)



# # Hyperparameter Tuning on Random forest

# In[34]:


# Define the model
rf = RandomForestRegressor(random_state=42)

# Define the parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Set up Grid Search with cross-validation
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Best parameters
best_parameters = grid_search.best_params_
print("Best Parameters: ", best_parameters)

# use these parameters to train final model
final_model = RandomForestRegressor(**best_parameters)
final_model.fit(X_train, y_train)




# In[ ]:




