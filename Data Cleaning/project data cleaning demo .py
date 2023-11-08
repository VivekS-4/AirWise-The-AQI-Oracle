#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install seaborn


# In[2]:


#pip install scipy


# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statistics
import warnings
warnings.filterwarnings("ignore")


# In[4]:


df = pd.read_csv("ontario-air-quality-sample.csv")
df


# In[5]:


100 - (len(df.dropna())/len(df))*100


# In[6]:


df.isnull().sum()


# In[7]:


df=df.dropna(subset=["SO2","CO"])


# In[8]:


df.info()


# In[9]:


df.isnull().sum()


# In[10]:


duplicate_rows=df.duplicated(subset=["Date","City","PM25","O3","NO2","SO2","CO"])
duplicate_counts = duplicate_rows.value_counts()
duplicate_counts

#so there are no duplicate values


# In[11]:


# Choose the column for which you want to create a histogram
column_name = "PM25"

# Create a histogram
plt.hist(df[column_name], bins=10, color='skyblue', edgecolor='black')

# Customize the plot (optional)
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')

# Show the plot
plt.show()


# In[12]:


column_name = "O3"

# Create a histogram
plt.hist(df[column_name], bins=10, color='skyblue', edgecolor='black')

# Customize the plot (optional)
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')

# Show the plot
plt.show()


# In[13]:


column_name = "CO"

# Create a histogram
plt.hist(df[column_name], bins=10, color='skyblue', edgecolor='black')

# Customize the plot (optional)
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')

# Show the plot
plt.show()


# In[14]:


column_name = "NO2"

# Create a histogram
plt.hist(df[column_name], bins=10, color='skyblue', edgecolor='black')

# Customize the plot (optional)
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')

# Show the plot
plt.show()


# In[15]:


column_name = "SO2"

# Create a histogram
plt.hist(df[column_name], bins=10, color='skyblue', edgecolor='black')

# Customize the plot (optional)
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')

# Show the plot
plt.show()


# In[16]:


df["PM25"] = pd.to_numeric(df["PM25"], errors="coerce")
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Remove outliers from the "PM25" column
df_cleaned = remove_outliers_iqr(df, "PM25")


# In[17]:


column_name = "PM25"

# Create a histogram
plt.hist(df[column_name], bins=10, color='green', edgecolor='black')

# Customize the plot (optional)
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')

# Show the plot
plt.show()


# In[18]:


df["SO2"] = pd.to_numeric(df["SO2"], errors="coerce")
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
df_cleaned = remove_outliers_iqr(df, "SO2")


# In[19]:


column_name = "SO2"
plt.hist(df[column_name], bins=10, color='green', edgecolor='black')
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')
plt.show()


# In[20]:


df["CO"] = pd.to_numeric(df["CO"], errors="coerce")
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
df_cleaned = remove_outliers_iqr(df, "CO")


# In[21]:


column_name = "CO"
plt.hist(df[column_name], bins=10, color='green', edgecolor='black')
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')
plt.show()


# In[22]:


df["O3"] = pd.to_numeric(df["O3"], errors="coerce")
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
df_cleaned = remove_outliers_iqr(df, "O3")


# In[23]:


column_name = "O3"
plt.hist(df[column_name], bins=10, color='green', edgecolor='black')
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')
plt.show()


# In[24]:


df["NO2"] = pd.to_numeric(df["NO2"], errors="coerce")
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
df_cleaned = remove_outliers_iqr(df, "NO2")


# In[25]:


column_name = "NO2"
plt.hist(df[column_name], bins=10, color='green', edgecolor='black')
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')
plt.show()


# In[ ]:




