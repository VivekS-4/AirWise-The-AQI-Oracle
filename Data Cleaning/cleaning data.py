#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statistics


# In[2]:


df = pd.read_csv("Hourly data copy.csv")
df


# In[3]:


100 - (len(df.dropna())/len(df))*100


# In[4]:


df.isnull().sum()


# In[5]:


# Calculate the median for each column
medians = df.median()

# Fill missing values with the respective column medians
df.fillna(medians, inplace=True)


# In[6]:


#to check if it is filled 
missing_values_count = df.isna().sum()
print("Number of missing values in each column:")
print(missing_values_count)


# In[7]:


# Check for duplicate rows
duplicates = df[df.duplicated()]

# Display the duplicate rows
if not duplicates.empty:
    print("Duplicate rows in the dataset:")
    print(duplicates)
else:
    print("No duplicate rows found in the dataset.")


# In[8]:


# Specify a Z-score or IQR threshold for outlier detection
z_score_threshold = 3
iqr_threshold = 1.5

# Create an empty DataFrame to store outlier flags for each column
outlier_flags = pd.DataFrame()

# Loop through each column in your DataFrame
for column in df.columns:
    # Check the data type of the column
    if np.issubdtype(df[column].dtype, np.number):
        # Calculate Z-scores and IQR for each numeric column
        z_scores = np.abs(stats.zscore(df[column]))
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        # Identify outliers based on thresholds
        z_score_outliers = z_scores > z_score_threshold
        iqr_outliers = (df[column] < Q1 - iqr_threshold * IQR) | (df[column] > Q3 + iqr_threshold * IQR)

        # Combine Z-score and IQR outlier flags
        combined_outliers = z_score_outliers | iqr_outliers

        # Add the outlier flags for the current column to the outlier_flags DataFrame
        outlier_flags[column] = combined_outliers

# Now, outlier_flags contains a binary flag (True/False) for each data point in your dataset
# indicating whether it's an outlier for the corresponding column.

# You can choose how to handle these outliers, whether by removing them or applying specific treatments.


# In[9]:


outlier_counts = outlier_flags.sum()
print(outlier_counts)


# In[10]:


print(outlier_flags)


# In[11]:


df.to_csv('hourly_data.csv', index=False)


# In[12]:


import os

file_path = 'hourly_data.csv'  # Replace with the actual file path or name
if os.path.isfile(file_path):
    print("The file has been saved successfully.")
else:
    print("The file could not be found. Check the file path and saving process.")


# In[ ]:





# In[ ]:




