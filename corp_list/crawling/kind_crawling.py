import pandas as pd
import csv

from utils import get_file_path

def kind_crawling():
    #open web-xls
    url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
    yuga_url = f'{url}&marketType=stockMkt'
    kosdaq_url = f'{url}&marketType=kosdaqMkt'
    yuga_krx = pd.read_html(yuga_url, header=0)[0]
    yuga_krx['시장'] = 'KOSPI'
    kosdaq_krx = pd.read_html(kosdaq_url, header=0)[0]
    kosdaq_krx['시장'] = 'KOSDAQ'
    
    krx = pd.concat([yuga_krx, kosdaq_krx], axis=0)

    krx = krx[['종목코드', '회사명', '업종', '주요제품', '상장일', '결산월', '대표자명', '홈페이지', '지역', '시장']]
    krx = krx.rename(columns={
        '종목코드': 'code',
        '회사명': 'company',
        '업종': 'Industry',
        '주요제품': 'Product',
        '상장일': 'listing_date',
        '결산월': 'Settlement_month',
        '대표자명': 'ceo',
        '홈페이지': 'homepage',
        '지역': 'area',
        '시장': 'market'})

    krx = krx.sort_values(by='code')

    krx.code = krx.code.map('{:06d}'.format) #6자리숫자 형식
    krxList = krx[['code', 'company', 'market']]

    #write CSV
    file_path = get_file_path(folder='data', file_name='kind-company-', file_ext='.csv')
    
    with open(file=file_path, mode='w', encoding='utf-8-sig', newline='') as f:
        print("Crawling KIND corp datas...")
        csv_f = csv.writer(f)
        for i in range(len(krxList)):
            value = [krxList.code.values[i], krxList.company.values[i], krxList.market.values[i]]
            csv_f.writerow(value)
    
    print(f"{len(krxList)} corp info downloaded.\n")

if __name__ == "__main__":
    kind_crawling()