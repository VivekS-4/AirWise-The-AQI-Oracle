#!/usr/bin/env python
# coding: utf-8

# In[18]:


from lxml import html
import requests
from datetime import date, timedelta
import csv
import pandas as pd
import numpy as np


# In[20]:


headers = {
    'authority': 'www.airqualityontario.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'referer': 'https://www.airqualityontario.com/history/summary.php',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}


# In[19]:


dates = []
start_date = date(2017, 1, 1)
end_date = date(2023, 10, 16)
delta = timedelta(days=1)
while start_date <= end_date:
    dates.append(start_date.strftime("%Y-%m-%d"))
    start_date += delta


# In[79]:


city = []
O3 = []
PM25 = []
NO2 = []
SO2 = []
CO = []
date = []
qa_caption = []
qa_date_text = []
count = 1

for i in dates[:2]:
    print(f"2480/{count}")
    count += 1
    spl = i.split('-')
    (year, month, day) = (spl[0], spl[1], spl[2])
    params = {
        'start_day': day,
        'start_month': month,
        'start_year': year,
        'my_hour': '20',
        'Submit': 'Update',
        'pol': '251',
    }

    response = requests.get('https://www.airqualityontario.com/history/summary.php', params=params, headers=headers)
    tree = html.fromstring(response.content)
    rows = tree.xpath('//table[@class="resourceTable"]/tbody/tr')
    qa_c = tree.xpath('//table/caption/text()')[0]
    qa_d = qa_c.replace('Air Pollutant 1-Hour Concentrations For ',
                        '').replace(', 8:00 pm EST', '')
    
    for row in rows:
        pol_data = [i for i in row.xpath('td//text()') if i != ' ']
        city.append(pol_data[0])
        O3.append(pol_data[1])
        PM25.append(pol_data[2])
        NO2.append(pol_data[3])
        SO2.append(pol_data[4])
        CO.append(pol_data[5])
        qa_caption.append(qa_c)
        qa_date_text.append(qa_d)
        date.append(i)
        
pol_dict = {'Date':date, 'City':city, 'O3':O3, 'PM25':PM25, 'NO2':NO2, 'SO2':SO2, 'CO':CO, 'qa_caption':qa_caption, 'qa_date_text':qa_date_text}
df = pd.DataFrame(pol_dict)
df.replace(to_replace=['\xa0', 'N/A'], value=np.nan, inplace=True)


# In[80]:


df


# In[70]:


df.to_csv('Pollutant_Data_Ontario.csv', index=False, 
          quoting=csv.QUOTE_ALL, encoding='utf-8')


# In[ ]:




