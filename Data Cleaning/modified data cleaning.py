#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as stats
import statistics


# In[2]:


df= pd.read_csv("Hourly data.csv")
df


# In[3]:


100 - (len(df.dropna())/len(df))*100


# In[4]:


df.isnull().sum()


# In[5]:


df.info


# In[6]:


d_types = df.dtypes
d_types


# In[7]:


columns_to_convert = [
    'SO2-H01', 'SO2-H02', 'SO2-H03', 'SO2-H04', 'SO2-H05', 'SO2-H06', 'SO2-H07', 'SO2-H08', 'SO2-H09', 'SO2-H10',
    'SO2-H11', 'SO2-H12', 'SO2-H13', 'SO2-H14', 'SO2-H15', 'SO2-H16', 'SO2-H17', 'SO2-H18', 'SO2-H19', 'SO2-H20',
    'SO2-H21', 'SO2-H22', 'SO2-H23', 'SO2-H24',
    'CO-H01', 'CO-H02', 'CO-H03', 'CO-H04', 'CO-H05', 'CO-H06', 'CO-H07', 'CO-H08', 'CO-H09', 'CO-H10', 'CO-H11',
    'CO-H12', 'CO-H13', 'CO-H14', 'CO-H15', 'CO-H16', 'CO-H17', 'CO-H18', 'CO-H19', 'CO-H20', 'CO-H21', 'CO-H22',
    'CO-H23', 'CO-H24',
    'NO-H01', 'NO-H02', 'NO-H03', 'NO-H04', 'NO-H05', 'NO-H06', 'NO-H07', 'NO-H08', 'NO-H09', 'NO-H10', 'NO-H11',
    'NO-H12', 'NO-H13', 'NO-H14', 'NO-H15', 'NO-H16', 'NO-H17', 'NO-H18', 'NO-H19', 'NO-H20', 'NO-H21', 'NO-H22',
    'NO-H23', 'NO-H24',
    'NO2-H01', 'NO2-H02', 'NO2-H03', 'NO2-H04', 'NO2-H05', 'NO2-H06', 'NO2-H07', 'NO2-H08', 'NO2-H09', 'NO2-H10',
    'NO2-H11', 'NO2-H12', 'NO2-H13', 'NO2-H14', 'NO2-H15', 'NO2-H16', 'NO2-H17', 'NO2-H18', 'NO2-H19', 'NO2-H20',
    'NO2-H21', 'NO2-H22', 'NO2-H23', 'NO2-H24',
    'O3-H01', 'O3-H02', 'O3-H03', 'O3-H04', 'O3-H05', 'O3-H06', 'O3-H07', 'O3-H08', 'O3-H09', 'O3-H10', 'O3-H11',
    'O3-H12', 'O3-H13', 'O3-H14', 'O3-H15', 'O3-H16', 'O3-H17', 'O3-H18', 'O3-H19', 'O3-H20', 'O3-H21', 'O3-H22',
    'O3-H23', 'O3-H24',
    'PM2.5-H01', 'PM2.5-H02', 'PM2.5-H03', 'PM2.5-H04', 'PM2.5-H05', 'PM2.5-H06', 'PM2.5-H07', 'PM2.5-H08',
    'PM2.5-H09', 'PM2.5-H10', 'PM2.5-H11', 'PM2.5-H12', 'PM2.5-H13', 'PM2.5-H14', 'PM2.5-H15', 'PM2.5-H16', 'PM2.5-H17',
    'PM2.5-H18', 'PM2.5-H19', 'PM2.5-H20', 'PM2.5-H21', 'PM2.5-H22', 'PM2.5-H23', 'PM2.5-H24',
    'NOx-H01', 'NOx-H02', 'NOx-H03', 'NOx-H04', 'NOx-H05', 'NOx-H06', 'NOx-H07', 'NOx-H08', 'NOx-H09', 'NOx-H10',
    'NOx-H11', 'NOx-H12', 'NOx-H13', 'NOx-H14', 'NOx-H15', 'NOx-H16', 'NOx-H17', 'NOx-H18', 'NOx-H19', 'NOx-H20',
    'NOx-H21', 'NOx-H22', 'NOx-H23', 'NOx-H24'
]

# Convert specified columns to float
df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')

print(df)


# In[8]:


d_types = df.dtypes
d_types


# In[9]:


df.shape


# In[10]:


df_filled = df.fillna(df.median())
print(df_filled)


# In[11]:


100 - (len(df_filled.dropna())/len(df_filled))*100


# In[12]:


columns_to_plot1 = [
    'SO2-H01', 'SO2-H02', 'SO2-H03', 'SO2-H04', 'SO2-H05', 'SO2-H06', 'SO2-H07', 'SO2-H08', 'SO2-H09', 'SO2-H10',
    'SO2-H11', 'SO2-H12', 'SO2-H13', 'SO2-H14', 'SO2-H15', 'SO2-H16', 'SO2-H17', 'SO2-H18', 'SO2-H19', 'SO2-H20',
    'SO2-H21', 'SO2-H22', 'SO2-H23', 'SO2-H24',
]

# Subset the DataFrame to include only the specified columns
subset_df = df[columns_to_plot1]

# Create a boxplot using Seaborn
plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
sns.set(style="whitegrid")  # Set the style of the boxplot

# Draw the boxplot
sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[13]:


columns_to_plot2 = ['CO-H01', 'CO-H02', 'CO-H03', 'CO-H04', 'CO-H05', 'CO-H06', 'CO-H07', 'CO-H08', 'CO-H09', 'CO-H10', 'CO-H11',
    'CO-H12', 'CO-H13', 'CO-H14', 'CO-H15', 'CO-H16', 'CO-H17', 'CO-H18', 'CO-H19', 'CO-H20', 'CO-H21', 'CO-H22',
    'CO-H23', 'CO-H24'
]

# Subset the DataFrame to include only the specified columns
subset_df = df[columns_to_plot2]

# Create a boxplot using Seaborn
plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
sns.set(style="whitegrid")  # Set the style of the boxplot

# Draw the boxplot
sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[14]:


columns_to_plot3 = ['NO-H01', 'NO-H02', 'NO-H03', 'NO-H04', 'NO-H05', 'NO-H06', 'NO-H07', 'NO-H08', 'NO-H09', 'NO-H10', 'NO-H11',
    'NO-H12', 'NO-H13', 'NO-H14', 'NO-H15', 'NO-H16', 'NO-H17', 'NO-H18', 'NO-H19', 'NO-H20', 'NO-H21', 'NO-H22',
    'NO-H23', 'NO-H24',
]

# Subset the DataFrame to include only the specified columns
subset_df = df[columns_to_plot3]

# Create a boxplot using Seaborn
plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
sns.set(style="whitegrid")  # Set the style of the boxplot

# Draw the boxplot
sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[15]:


columns_to_plot4 = ['NO2-H01', 'NO2-H02', 'NO2-H03', 'NO2-H04', 'NO2-H05', 'NO2-H06', 'NO2-H07', 'NO2-H08', 'NO2-H09', 'NO2-H10',
    'NO2-H11', 'NO2-H12', 'NO2-H13', 'NO2-H14', 'NO2-H15', 'NO2-H16', 'NO2-H17', 'NO2-H18', 'NO2-H19', 'NO2-H20',
    'NO2-H21', 'NO2-H22', 'NO2-H23', 'NO2-H24',
]

# Subset the DataFrame to include only the specified columns
subset_df = df[columns_to_plot4]

# Create a boxplot using Seaborn
plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
sns.set(style="whitegrid")  # Set the style of the boxplot

# Draw the boxplot
sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[16]:


columns_to_plot5 = ['O3-H01', 'O3-H02', 'O3-H03', 'O3-H04', 'O3-H05', 'O3-H06', 'O3-H07', 'O3-H08', 'O3-H09', 'O3-H10', 'O3-H11',
    'O3-H12', 'O3-H13', 'O3-H14', 'O3-H15', 'O3-H16', 'O3-H17', 'O3-H18', 'O3-H19', 'O3-H20', 'O3-H21', 'O3-H22',
    'O3-H23', 'O3-H24',
]

# Subset the DataFrame to include only the specified columns
subset_df = df[columns_to_plot5]

# Create a boxplot using Seaborn
plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
sns.set(style="whitegrid")  # Set the style of the boxplot

# Draw the boxplot
sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[17]:


columns_to_plot6 = [ 'PM2.5-H01', 'PM2.5-H02', 'PM2.5-H03', 'PM2.5-H04', 'PM2.5-H05', 'PM2.5-H06', 'PM2.5-H07', 'PM2.5-H08',
    'PM2.5-H09', 'PM2.5-H10', 'PM2.5-H11', 'PM2.5-H12', 'PM2.5-H13', 'PM2.5-H14', 'PM2.5-H15', 'PM2.5-H16', 'PM2.5-H17',
    'PM2.5-H18', 'PM2.5-H19', 'PM2.5-H20', 'PM2.5-H21', 'PM2.5-H22', 'PM2.5-H23', 'PM2.5-H24',
]

# Subset the DataFrame to include only the specified columns
subset_df = df[columns_to_plot6]

# Create a boxplot using Seaborn
plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
sns.set(style="whitegrid")  # Set the style of the boxplot

# Draw the boxplot
sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[18]:


columns_to_plot7 = [  'NOx-H01', 'NOx-H02', 'NOx-H03', 'NOx-H04', 'NOx-H05', 'NOx-H06', 'NOx-H07', 'NOx-H08', 'NOx-H09', 'NOx-H10',
    'NOx-H11', 'NOx-H12', 'NOx-H13', 'NOx-H14', 'NOx-H15', 'NOx-H16', 'NOx-H17', 'NOx-H18', 'NOx-H19', 'NOx-H20',
    'NOx-H21', 'NOx-H22', 'NOx-H23', 'NOx-H24'
]

# Subset the DataFrame to include only the specified columns
subset_df = df[columns_to_plot7]

# Create a boxplot using Seaborn
plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
sns.set(style="whitegrid")  # Set the style of the boxplot

# Draw the boxplot
sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[19]:


subset_df = df[columns_to_plot1]

tukey_multiplier = 1

# Define a function to identify and remove outliers using Tukey's fences
def remove_outliers_tukey(column):
   Q1 = subset_df[column].quantile(0.40)
   Q3 = subset_df[column].quantile(0.60)
   IQR = Q3 - Q1
   lower_fence = Q1 - tukey_multiplier * IQR
   upper_fence = Q3 + tukey_multiplier * IQR
   subset_df[column] = subset_df[column][(subset_df[column] >= lower_fence) & (subset_df[column] <= upper_fence)]

# Remove outliers using Tukey's fences for each column
for column in columns_to_plot1:
   remove_outliers_tukey(column)
df[columns_to_plot1] = subset_df


# In[20]:


plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data (Outliers Removed)")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[21]:


#outliers of CO
subset_df = df[columns_to_plot2]

tukey_multiplier = 1

# Define a function to identify and remove outliers using Tukey's fences
def remove_outliers_tukey(column):
    Q1 = subset_df[column].quantile(0.30)
    Q3 = subset_df[column].quantile(0.70)
    IQR = Q3 - Q1
    lower_fence = Q1 - tukey_multiplier * IQR
    upper_fence = Q3 + tukey_multiplier * IQR
    subset_df[column] = subset_df[column][(subset_df[column] >= lower_fence) & (subset_df[column] <= upper_fence)]

# Remove outliers using Tukey's fences for each column
for column in columns_to_plot2:
    remove_outliers_tukey(column)
df[columns_to_plot2] = subset_df


# In[22]:


plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data (Outliers Removed)")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[23]:


#outliers of NO
subset_df = df[columns_to_plot3]

tukey_multiplier = 1

# Define a function to identify and remove outliers using Tukey's fences
def remove_outliers_tukey(column):
    Q1 = subset_df[column].quantile(0.40)
    Q3 = subset_df[column].quantile(0.60)
    IQR = Q3 - Q1
    lower_fence = Q1 - tukey_multiplier * IQR
    upper_fence = Q3 + tukey_multiplier * IQR
    subset_df[column] = subset_df[column][(subset_df[column] >= lower_fence) & (subset_df[column] <= upper_fence)]

# Remove outliers using Tukey's fences for each column
for column in columns_to_plot3:
    remove_outliers_tukey(column)
df[columns_to_plot3] = subset_df


# In[24]:


plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data (Outliers Removed)")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[25]:


#outliers of NO2
subset_df = df[columns_to_plot4]

tukey_multiplier = 1

# Define a function to identify and remove outliers using Tukey's fences
def remove_outliers_tukey(column):
    Q1 = subset_df[column].quantile(0.35)
    Q3 = subset_df[column].quantile(0.65)
    IQR = Q3 - Q1
    lower_fence = Q1 - tukey_multiplier * IQR
    upper_fence = Q3 + tukey_multiplier * IQR
    subset_df[column] = subset_df[column][(subset_df[column] >= lower_fence) & (subset_df[column] <= upper_fence)]

# Remove outliers using Tukey's fences for each column
for column in columns_to_plot4:
    remove_outliers_tukey(column)
df[columns_to_plot4] = subset_df


# In[26]:


plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data (Outliers Removed)")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[27]:


#outliers of O3
subset_df = df[columns_to_plot5]
tukey_multiplier = 1

# Define a function to identify and remove outliers using Tukey's fences
def remove_outliers_tukey(column):
    Q1 = subset_df[column].quantile(0.25)
    Q3 = subset_df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_fence = Q1 - tukey_multiplier * IQR
    upper_fence = Q3 + tukey_multiplier * IQR
    subset_df[column] = subset_df[column][(subset_df[column] >= lower_fence) & (subset_df[column] <= upper_fence)]

# Remove outliers using Tukey's fences for each column
for column in columns_to_plot5:
    remove_outliers_tukey(column)
df[columns_to_plot5] = subset_df


# In[28]:


plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data (Outliers Removed)")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[29]:


#outliers of PM 2.5
subset_df = df[columns_to_plot6]
tukey_multiplier = 1

# Define a function to identify and remove outliers using Tukey's fences
def remove_outliers_tukey(column):
    Q1 = subset_df[column].quantile(0.25)
    Q3 = subset_df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_fence = Q1 - tukey_multiplier * IQR
    upper_fence = Q3 + tukey_multiplier * IQR
    subset_df[column] = subset_df[column][(subset_df[column] >= lower_fence) & (subset_df[column] <= upper_fence)]

# Remove outliers using Tukey's fences for each column
for column in columns_to_plot6:
    remove_outliers_tukey(column)
df[columns_to_plot6] = subset_df


# In[30]:


plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data (Outliers Removed)")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[31]:


#outliers of NOX
subset_df = df[columns_to_plot7]
tukey_multiplier = 1

# Define a function to identify and remove outliers using Tukey's fences
def remove_outliers_tukey(column):
    Q1 = subset_df[column].quantile(0.35)
    Q3 = subset_df[column].quantile(0.65)
    IQR = Q3 - Q1
    lower_fence = Q1 - tukey_multiplier * IQR
    upper_fence = Q3 + tukey_multiplier * IQR
    subset_df[column] = subset_df[column][(subset_df[column] >= lower_fence) & (subset_df[column] <= upper_fence)]

# Remove outliers using Tukey's fences for each column
for column in columns_to_plot7:
    remove_outliers_tukey(column)
df[columns_to_plot7] = subset_df


# In[32]:


plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

sns.boxplot(data=subset_df, width=0.5)
plt.title("Boxplot of Air Quality Data (Outliers Removed)")
plt.xlabel("Hourly Intervals")
plt.ylabel("Concentration")

plt.show()


# In[37]:


df_filled.to_csv('cleaned_data.csv', index=False)


# In[36]:


import os

file_path = 'cleaned_data.csv'  
if os.path.isfile(file_path):
    print("The file has been saved successfully.")
else:
    print("The file could not be found. Check the file path and saving process.")


# In[ ]:




