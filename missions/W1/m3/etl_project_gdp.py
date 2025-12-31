from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import sqlite3
from datetime import datetime


def main(user_agent: str, save_options: list[str]) -> None:
    """
    Args:
        user_agent: your user_agent string
        save_options: 'json' or 'db'
    """
    try:
        log('[INFO] Process started: GDP Data ETL')
        gdp_table = extract_gdp_from_wiki(user_agent)
        df = transfrom_data(gdp_table)
        country_region_map = get_country_region_map()
        load_data(df, save_options, country_region_map)
        log('[INFO] Process completed succesfully')
    except Exception as e:
        log(f'[ERROR] Pipeline stopped: {e}')
    

def extract_gdp_from_wiki(user_agent: str) -> list:
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
    header = {'User-Agent': user_agent}
    html_content = fetch_gdp_data(url, header)

    # html 에서 gdp 테이블 부분 검색하여 추출 / 테이블의 각 행을 리스트에 담아 리턴
    soup = BeautifulSoup(html_content,'html.parser')
    gdp_table = soup.find('table', class_='wikitable')
    if not gdp_table:
        raise ValueError('[ERROR] Could not find the GDP table in the HTML content.')
    table_rows = gdp_table.find_all('tr')
    log(f'[INFO] Extract Data complete')
    return table_rows

def fetch_gdp_data(url: str, header: dict) -> str:
    try:
        response = requests.get(url=url, headers=header, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as e:
        log(f'[ERROR] HTTP GET: {e}')
        raise

def transfrom_data(rows: list) -> pd.DataFrame:
    ''' Convert html to DataFrame'''
    data=[]
    for row in rows:
        # 각주 부분([ ]) 제거
        cols = [re.sub(r'\[.*?\]', '',ele.text).strip() for ele in row.find_all(['td', 'th'])]
        data.append(cols)

    df = pd.DataFrame(data[1:], columns=data[0])
    log(f'[INFO] HTML -> DataFrame conversion complete')
    return df



def load_data(df: pd.DataFrame, save_options: list[str], country_region_map: dict) -> None:
    ''' print and save GDP data '''
    # 테이블의 1열(국가정보), 2열(최신 IMF gdp 현황)만 사용
    df = df.iloc[1:,0:2]
    df.iloc[:,1] = df.iloc[:,1].apply(convert_unit_to_B)
    # IMF gdp 현황의 값이 NA인 국가 제거
    df = df.dropna()
    table_name = df.columns[-1]
    df.columns = ['Country','GDP_USD_billion']

    #GDP가 100B USD이상이 되는 국가만을 구해서 화면에 출력
    filtered_df = df[df.iloc[:,1] >= 100]
    print(filtered_df)
    #각 Region별로 top5 국가의 GDP 평균을 구해서 화면에 출력
    region_added_df = df.assign(Region = lambda x: x['Country'].map(country_region_map))
    region_added_df.dropna()
    region_added_df['GDP_USD_billion'] = pd.to_numeric(region_added_df['GDP_USD_billion'])
    top5_Average = region_added_df.groupby('Region')['GDP_USD_billion'].apply(lambda x: round(x.nlargest(5).mean(),2))
    print(top5_Average)

    if 'json' in save_options:
        save_json(df)
    if 'db' in save_options:
        save_sqlite(df)

def save_json(df: pd.DataFrame) -> None:
    df.to_json('Countries_by_GDP.json', orient='records', indent=4)
    log('[INFO] GDP data exported to JSON file')

def save_sqlite(df: pd.DataFrame) -> None:
    conn = sqlite3.connect('World_Economies.db')
    df.to_sql('Countries_by_GDP', conn, index=False, if_exists='replace')
    log('[INFO] GDP table created successfully in SQLite')
    conn.close()

def log(message: str) -> None:
    timestamp_format = '%Y-%B-%d-%H-%M-%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    
    with open('etl_project_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{timestamp}, {message}\n")

def convert_unit_to_B(money_str: str) -> float:
    """ 달러 단위 변환, 값이 NA인 경우 None으로 변경 """
    if '(' in money_str or ')' in money_str:
        return None
    converted_str = re.sub(r'[^\d.]', '', str(money_str))
    if not converted_str:
        return None
    return round(float(converted_str)/1000, 2)

def get_country_region_map() -> dict[str:str]:
    df = pd.read_csv('country_data.tsv', sep='\t')
    result= df.set_index('name_short')['Continent_7'].to_dict()
    return result

if __name__ == "__main__":
    main(user_agent='Chrome/143.0.0.0', save_options=['json', 'db'])