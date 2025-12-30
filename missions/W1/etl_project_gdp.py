from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import sqlite3
from datetime import datetime

def extract_gdp_from_wiki(user_agent: str) -> list:
    '''
    
    '''
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    header = {'User-Agent': user_agent}
    response = requests.get(url, headers=header)
    html_content = response.text

    soup = BeautifulSoup(html_content,"html.parser")
    gdp_table = soup.find("table", class_="wikitable")
    table_rows = gdp_table.find_all("tr")
    return table_rows

def transfrom_data(rows: list) -> pd.DataFrame:
    '''
    '''
    data=[]
    for row in rows:
        cols = [re.sub(r'\[.*?\]', '',ele.text).strip() for ele in row.find_all(["td", "th"])]
        data.append(cols)
    
    df = pd.DataFrame(data[1:], columns=data[0])
    return df



def load_data(df: pd.DataFrame, save_options: list) -> None:
    '''
    '''
    df = df.iloc[1:,0:2]
    df.iloc[:,1] = df.iloc[:,1].apply(convert_unit_to_B)
    df.dropna()
    table_name = df.columns[-1]
    df.columns = ['Country','GDP_USD_billion']
    filtered_df = df[df.iloc[:,1] >= 100]
    print(filtered_df)

    if 'json' in save_options:
        save_json(df)
    elif 'db' in save_options:
        save_sqlite(df)

def save_json(df: pd.DataFrame) -> None:
    df.to_json('Countries_by_GDP.json', orient='records', indent=4)

def save_sqlite(df: pd.DataFrame) -> None:
    conn = sqlite3.connect('World_Economies.db')
    df.to_sql('Countries_by_GDP', conn, index=False)
    conn.close()

def log(message: str) -> None:
    #시간 포맷 설정 (Year-Monthname-Day-Hour-Minute-Second)
    timestamp_format = '%Y-%B-%d-%H-%M-%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    
    with open('etl_project_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{timestamp}, {message}\n")

def convert_unit_to_B(money_str: str) -> float:
    # 단위 변환, 값이 NA인 경우 None으로 변경
    converted_str = re.sub(r'[^\d.]', '', str(money_str))
    if not converted_str:
        return None
    return round(float(converted_str)/1000, 2)

if __name__ == "__main__":
    gdp_table = extract_gdp_from_wiki(user_agent='Chrome/143.0.0.0')
    df = transfrom_data(gdp_table)
    load_data(df, save_options=['db'])