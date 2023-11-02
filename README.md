
## 다트 크롤링

### 파일 구조
```
crawling/  
    ├── README.md  
    ├── requirements.txt  
    ├── corp_list/  
    │   ├── make_corp_list.py  
    │   ├── crawling/  
    │   │   ├── dart_crawling.py  
    │   │   ├── kind_crawling.py  
    │   ├── data/ # corp_list/make_corp_list.py 실행시 생성  
    │   │   ├── CORPCODE.xml   
    │   │   ├── company-{yyyy}-{mm}-{dd}.csv  
    │   │   ├── dart-company-{yyyy}-{mm}-{dd}.csv  
    │   │   ├── kind-company-{yyyy}-{mm}-{dd}.csv  
    ├── dart/  
    │   ├── dart_crawler.py  
    │   ├── get_dart_info.py  
    │   ├── get_executives.py  
    │   ├── utils/  
    │   │   ├── utils.py  
    │   ├── data/ # dart/dart_crawler.py 실행 시 폴더 및 하위 데이터들 생성  
```


```
// pandas로 csv 조작 모듈
extract_year.py: 2015-12-30 -> 2015 추출해서 저장
filter_csv.py: csv 파일 내에서 특정 헤더만 추출해서 저장
merge_csv.py: 여러 csv 파일을 하나로 합침

get_corpcode_from_dart.py: dart API 요청 보낼 시 필요한 corp_code를 xml 내에서 찾는 모듈
get_dart_info.py: 소액주주, 자사주, 최대주주 주식 수 등 개별 행에 1개씩 있는 데이터
get_executives.py: 임원목록, 최대주주현황, 타법인출자현황 등 개별 행에 여러 개씩 있는 데이터를 연도, 분기별로 크롤링

dart_crawler.py: dart api crawling 최상위, 기간을 지정해 기간 별 크롤링 가능


```


### install
```bash
python3 -m venv venv
pip install -r requirements.txt
```

### RUN

```bash
python filter_csv.py --csv_filename data/2015_2017-상장사.csv --headers 종목코드
python merge_csv.py --csv_filenames data/2015_2017-상장사.csv data/2018_2020-상장사.csv

python get_dart_info.py --csv_filename data/상장사-corp_code.csv
python get_executives_api.py --api 임원목록 --csv_filename data/company-{yyyy}-{mm}-{dd}.csv --year 2023 --quarter 2
python dart_crawler.py --api 임원목록 --csv_filename data/company-{yyyy}-{mm}-{dd}.csv --start_year 2022 --start_quarter 1 --end_year 2023 --end_quarter 2
```

### TODO
- [ ] 1 혹은 다 여부에 따른 추출 쉽게 조절하게 만들기