
## 다트 크롤링
OpenDART API 내의 사업보고서 주요정보란의 데이터를 받아오기 위한 데이터 추출 프로그램입니다.

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
    │   │   ├── extract_year.py  
    │   │   ├── filter_csv.py  
    │   │   ├── merge_csv.py  
    │   │   ├── utils.py  
    │   ├── data/ # dart/dart_crawler.py 실행 시 폴더 및 하위 데이터들 생성
    │   │   ├── 임원목록/ # example
```

```
// corp_list
crawling/dart_crawling.py: dart의 상장 법인 리스트 가져오기
crawling/kind_crawling.py: Kind의 상장 법인 리스트 가져오기
make_corp_list.py: 수행 시, 두 데이터를 가져와서 join을 통해 해당 날짜 기준 상장법인 리스트 데이터 생성

// dart
get_corpcode_from_dart.py: dart API 요청 보낼 시 필요한 corp_code를 xml 내에서 찾는 모듈
get_dart_info.py: 소액주주, 자사주, 최대주주 주식 수 등 개별 행에 1개씩 있는 데이터
get_executives.py: 임원목록, 최대주주현황, 타법인출자현황 등 개별 행에 여러 개씩 있는 데이터를 연도, 분기별로 크롤링

dart_crawler.py: dart api crawling 최상위 기능, 기간을 지정해 기간 별 크롤링 가능
```

### install
```bash
python3 -m venv venv
pip install -r requirements.txt
```

### RUN

```bash
# corp_list
python make_corp_list.py # 수행 시, 해당 날짜 기준 상장법인 리스트 데이터 생성

# dart
python filter_csv.py --csv_filename data/2015_2017-상장사.csv --headers 종목코드
python merge_csv.py --csv_filenames data/2015_2017-상장사.csv data/2018_2020-상장사.csv

python get_dart_info.py --api 소액주주현황 --csv_filename data/company-{yyyy}-{mm}-{dd}.csv --year 2023 --quarter 2
python get_executives_api.py --api 임원목록 --csv_filename data/company-{yyyy}-{mm}-{dd}.csv --year 2023 --quarter 2
python dart_crawler.py --api 임원목록 --csv_filename data/company-{yyyy}-{mm}-{dd}.csv --start_year 2022 --start_quarter 1 --end_year 2023 --end_quarter 2
```

### ERROR
```
종목명's data is missing: api response가 정상이 아님 -> 해당 연도, 분기의 데이터 자체에 해당 기업이 없음   
종목명's data returns None: api response는 정상 -> 해당 연도, 분기의 요청 데이터가 비어 있는 경우
```

### USES
- args를 통해 해당하는 func 매칭해서 반환하는 return_api에 원하는 api에 대한 함수 (get~, marshall~) 추가 후 run  
- root 디렉토리에 config.json 또는 환경변수로 API_KEY 추가해서 사용 가능