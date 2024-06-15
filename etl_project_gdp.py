import pandas as pd
import requests
import sqlite3 
from bs4 import BeautifulSoup 

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
db_name = 'World_Economies.db'
db_table='Countries_by_GDP'
csv_path= r'C:\Users\A0149938\Documents\Brayam\Cousera\scripts\Countries_by_GDP.json'
df = pd.DataFrame(columns=['Country','GDP_USD_billion'])
USD = 0 

hml_page=requests.get(url).text
data = BeautifulSoup(html_page, 'html.parse')

tables = data.find_all('tbody')
rows= tables[0].find_all('tr')

for row in rows:
    if USD > 1000000:
        col = row.find_all('td')
    if len(col)!=0:
        data_dict={'Country':col[0].contents[0],
                   'GDP_USD_billion':col[1].contents[0]}
        USD = data_dict['GDP_USD_billion']
        df1 = pd.DataFrame(data_dict, index[0])
        df=pd.concat([df, df1], ignore_index=True)
    else:
        break
print(df)