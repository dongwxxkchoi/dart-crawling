import pandas as pd
import csv
import os
from datetime import datetime

#open web-xls
url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
krx = pd.read_html(url, header=0)[0]

krx = krx[['종목코드', '회사명', '업종', '주요제품','상장일', '결산월', '대표자명', '홈페이지', '지역']]
krx = krx.rename(columns={
    '종목코드': 'code',
    '회사명': 'company',
    '업종': 'Industry',
    '주요제품': 'Product',
    '상장일': 'listing_date',
    '결산월': 'Settlement_month',
    '대표자명': 'ceo',
    '홈페이지': 'homepage',
    '지역': 'area'})

krx = krx.sort_values(by='code')
krx.code = krx.code.map('{:06d}'.format)#6자리숫자 형식
krxList = krx[['code', 'company']]

#write CSV
today = datetime.today().strftime("%Y-%m-%d")
folder = 'data'
file_name = 'kind-company-'+today+'.csv'
file_path = os.path.join(folder, file_name)

with open(file=file_path, mode='w', encoding='utf-8-sig', newline='') as f:
    csv_f = csv.writer(f)
    for i in range(len(krxList)):
        value = [krxList.code.values[i], krxList.company.values[i]]
        csv_f.writerow(value)
    print(today)
    print(f"{len(krxList)} corp info downloaded.")