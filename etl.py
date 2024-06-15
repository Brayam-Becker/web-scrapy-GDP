import pandas as pd
import requests
import sqlite3 
from bs4 import BeautifulSoup 
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("process_log.log"),
                              logging.StreamHandler()])

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
db_name = 'World_Economies.db'
db_table='Countries_by_GDP'
csv_path= r'C:\Users\A0149938\Documents\Brayam\Cousera\scripts\Countries_by_GDP.json'
df = pd.DataFrame(columns=['Country','GDP_USD_billion'])
USD = 1000001

logging.info("Fetching the HTML page.")
html_page=requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

logging.info("Extracting data from the HTML page.")
tables = data.find_all('tbody')
rows= tables[2].find_all('tr')
col = rows[2].find_all('td')
for row in rows:
   dados = row.find_all('td')
   if len(dados)!=0:
      primeiracoluna = dados[0]
      tag_a = primeiracoluna.find_all('a')
      for tag in tag_a:
         country = tag.text.strip()
         if USD>1000000:
            data_dict={'Country':country,
                  'GDP_USD_billion':dados[2].contents[0].replace(',','')}
            df1 = pd.DataFrame(data_dict, index=[0])
            df=pd.concat([df, df1], ignore_index=True)

   
logging.info("Data extraction complete.")         
logging.info("DataFrame before conversion:\n%s", df.head())
df['GDP_USD_billion'] = pd.to_numeric(df['GDP_USD_billion'], errors='coerce')
logging.info("Converted GDP_USD_billion to numeric. DataFrame:\n%s", df.head())
df.to_json('D:\Docs Brayam\Documentos\Engenharia de dados\Coursera\projeto\Countries_by_GDP.json', orient='records', lines=True)
logging.info("Data saved to JSON file.")
db_name='World_Economies.db'
table_name='Countries_by_GDP'
sql_connection = sqlite3.connect(table_name)
df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
logging.info("Data saved to SQLite database.")
query_statment = F'SELECT Country FROM {table_name} where GDP_USD_billion > 1000000'
df_output= pd.read_sql(query_statment, sql_connection)
logging.info("Query executed. Result:\n%s", df_output)

sql_connection.close()
logging.info("SQLite connection closed.")