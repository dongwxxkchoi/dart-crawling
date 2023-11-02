import zipfile
import requests
import xml.etree.ElementTree as elemTree
import pandas as pd
import os
import json

from utils import get_file_path

def dart_crawling():
    API_URL = "https://opendart.fss.or.kr/api/corpCode.xml"

    if os.path.exists('../config.json'):
        with open('../config.json', 'r') as file:
            config_data = json.load(file)

        API_KEY = config_data['API_KEY']
    else:
        API_KEY = os.environ.get('API_KEY')


    response = requests.get(f"{API_URL}?crtfc_key={API_KEY}")

    file_path = get_file_path(folder='data', file_name='dart-company-', file_ext='.zip')
    print("Crawling DART corp datas...")

    if response.status_code == 200:
        print('connection good')
        with open(file_path, "wb") as f:
            f.write(response.content)
        f.close()


    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('data')

    tree = elemTree.parse('data/CORPCODE.xml')

    temp_list = []
    for data in tree.findall('./list'):
        temp = []
        for d in data:
            temp.append(d.text)
        temp_list.append(temp)

    corp_df = pd.DataFrame(temp_list)
    corp_df.columns = ["corp_code","corp_name","stock_code","modify_date"]
    file_path = get_file_path(folder='data', file_name='dart-company-', file_ext='.csv')
    corp_df.to_csv(file_path, index=False)

    print(f"{len(corp_df)} corp info downloaded.\n")