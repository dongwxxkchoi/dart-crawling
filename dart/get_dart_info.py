import argparse
from utils.utils import get_new_csv_filename, request_to_dart, iterate_csv, list_to_csv
import asyncio



def get_dict_by_key(response: list[dict], **kwargs) -> dict:
    for dictionary in response:
        if all(k in dictionary and dictionary[k] == v for k, v in kwargs.items()):
            return dictionary


def get_dict_with_max_value(response: list[dict], key):
    def parse_string_to_int(val: str) -> int:
        try:
            return int(val.replace(',', ''))
        except ValueError:
            return 0
    return max(response, key=lambda x: parse_string_to_int(x.get(key, 0)))


def marshall_total_compensation(response):
    element = get_dict_by_key(response, se='전체보수')
    return {'인원수': element['nmpr'],
            '보수 총액': element['mendng_totamt'],
            '1인 평균 보수 액': element['jan_avrg_mendng_am']}


def marshall_small_shareholders(response):
    element = get_dict_by_key(response, se='소액주주')
    return {'소액주주수': element['shrholdr_co'],
            '소액주주주식수': element['hold_stock_co'],
            '소액주주지분율': element['hold_stock_rate']}


# 이사 감사 전체의 보수현황
async def get_total_compensation(row):
    response = await request_to_dart('hmvAuditAllSttus.json', row)
    if response is None:
        return
    return marshall_total_compensation(response['list'])

# 소액 주주 현황
async def get_small_shareholders(row):
    response = await request_to_dart('mrhlSttus.json', row)
    if response is None:
        return
    return marshall_small_shareholders(response['list'])

def return_api(api):
    if api == '소액주주현황':
        return get_small_shareholders
    elif api == '이사감사전체보수':
        return get_total_compensation
    else:
        raise Exception("Wrong api name")

async def crawl_one_2_one(api, csv_filename, year, quarter):
    func = return_api(api) 
    results = await iterate_csv(csv_filename, year, quarter, func)
    new_csv_filename = get_new_csv_filename(csv_filename, api, year, quarter)
    list_to_csv(results, new_csv_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api', type=str, help='소액주주현황, 이사감사전체보수')
    parser.add_argument('--csv_filename', type=str, help='상장사 목록 csv')
    parser.add_argument('--year', type=str, help='년도')
    parser.add_argument('--quarter', type=str, help='분기(1,2,3,4)')

    args = parser.parse_args()
    import time
    a = time.time()
    asyncio.run(crawl_one_2_one(args.csv_filename))
    print(f"takes {time.time() - a}")