#!/usr/bin/env python
# coding: utf-8

# In[18]:


import requests
from bs4 import BeautifulSoup
import csv
import os
from tqdm import tqdm

def scrape_aqhidata(day, month, year, output_file, pbar):
    url = f"https://www.airqualityontario.com/aqhi/search.php?stationid=29000&show_day=1&start_day={day}&start_month={month}&start_year={year}&submit_search=Get+AQHI+Readings"

    #HTTP get request from URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # search table element with class 'resourceTable'
        table = soup.find('table', {'class': 'resourceTable'})

        if table:
    
            rows = table.find_all('tr')

            # Creating CSV file
            output_f = os.path.join(output_file, f'aqhi_data_{year}_{month}_{day}.csv')

            with open(output_f, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)

                for row in rows:
                    
                    cells = row.find_all(['td', 'th'])

                
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    csv_writer.writerow(row_data)

            pbar.update(1)  
        else:
            print("Table not found on the page")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def scrape_aqhidata_for_month_and_year(month, year, output_file, pbar):

    days_in_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30 if month in [4, 6, 9, 11] else 28

    with tqdm(total=days_in_month, desc=f'Data for {year}-{month}') as pbar_month:
        for day in range(1, days_in_month + 1):
            scrape_aqhidata(day, month, year, output_file, pbar_month)

def scrape_aqhidata_for_all_months_and_year(year, output_folder):
    
    with tqdm(total=12, desc=f'Data for {year}') as pbar_year:
        for month in range(1, 13):
            scrape_aqhidata_for_month_and_year(month, year, output_file, pbar_year)


year = 2022
output_f = 'Hamilton_Downtown'  
os.makedirs(output_file, exist_ok=True)
scrape_aqhidata_for_all_months_and_year(year, output_file) 



# In[19]:


import requests
from bs4 import BeautifulSoup
import csv
import os
from tqdm import tqdm

def scrape_aqhidata(day, month, year, output_file, pbar):
    url = f"https://www.airqualityontario.com/aqhi/search.php?stationid=29000&show_day=1&start_day={day}&start_month={month}&start_year={year}&submit_search=Get+AQHI+Readings"

    #HTTP get request from URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # search table element with class 'resourceTable'
        table = soup.find('table', {'class': 'resourceTable'})

        if table:
    
            rows = table.find_all('tr')

            # Creating CSV file
            output_f = os.path.join(output_file, f'aqhi_data_{year}_{month}_{day}.csv')

            with open(output_f, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)

                for row in rows:
                    
                    cells = row.find_all(['td', 'th'])

                
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    csv_writer.writerow(row_data)

            pbar.update(1)  
        else:
            print("Table not found on the page")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def scrape_aqhidata_for_month_and_year(month, year, output_file, pbar):

    days_in_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30 if month in [4, 6, 9, 11] else 28

    with tqdm(total=days_in_month, desc=f'Data for {year}-{month}') as pbar_month:
        for day in range(1, days_in_month + 1):
            scrape_aqhidata(day, month, year, output_file, pbar_month)

def scrape_aqhidata_for_all_months_and_year(year, output_folder):
    
    with tqdm(total=12, desc=f'Data for {year}') as pbar_year:
        for month in range(1, 13):
            scrape_aqhidata_for_month_and_year(month, year, output_file, pbar_year)


year = 2022
output_f = 'Hamilton_Mountain'  
os.makedirs(output_file, exist_ok=True)
scrape_aqhidata_for_all_months_and_year(year, output_file) 



# In[ ]:




