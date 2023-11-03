import argparse
import asyncio
from utils.utils import get_new_csv_filename, list_to_csv, request_to_dart, iterate_csv
import os
import json

def copied_list_of_dicts(list_of_dicts: list[dict]):
    copied_list_of_dicts = list_of_dicts.copy()
    for dictionary in copied_list_of_dicts:
        for key, value in dictionary.items():
            dictionary[key] = value.replace('\n', '')
    return copied_list_of_dicts


def marshall_executives(response):
    response = copied_list_of_dicts(response)
    return list(map(lambda element:
                    {'이름': element['nm'],
                     '생년월일': element['birth_ym'],
                     '성별': element['sexdstn'],
                     '직위': element['ofcps'],
                     '등기여부': element['rgist_exctv_at'],
                     '상근여부': element['fte_at'],
                     '담당업무': element['chrg_job'],
                     '최대주주와의관계': element['mxmm_shrholdr_relate'],
                     '재직기간': element['hffc_pd'],
                     '임기만료일': element['tenure_end_on']}, response))


def marshall_shareholders(response):
    response = copied_list_of_dicts(response)[:-2]
    try:
        result = list(map(lambda element:
                    {'접수번호': element['rcept_no'],
                     '법인구분': element['corp_cls'],
                     '고유번호': element['corp_code'],
                     '법인명': element['corp_name'],
                     '주식 종류': element['stock_knd'],
                     '성명': element['nm'],
                     '관계': element['relate'],
                     '기초 소유 주식 수': element['bsis_posesn_stock_co'],
                     '기초 소유 주식 지분 율': element['bsis_posesn_stock_qota_rt'],
                     '기말 소유 주식 수': element['trmend_posesn_stock_co'],
                     '기말 소유 주식 지분 율': element['trmend_posesn_stock_qota_rt'],
                     '비고': element['rm'],
                     }, response))
    except Exception:
        result = list(map(lambda element:
                    {'접수번호': element['rcept_no'],
                     '법인구분': element['corp_cls'],
                     '고유번호': element['corp_code'],
                     '법인명': element['corp_name'],
                     '주식 종류': element['stock_knd'],
                     '성명': element['nm'],
                     '기초 소유 주식 수': element['bsis_posesn_stock_co'],
                     '기초 소유 주식 지분 율': element['bsis_posesn_stock_qota_rt'],
                     '기말 소유 주식 수': element['trmend_posesn_stock_co'],
                     '기말 소유 주식 지분 율': element['trmend_posesn_stock_qota_rt'],
                     '비고': element['rm'],
                     }, response))
    
    return result

def marshall_investment(response):
    response = copied_list_of_dicts(response)
    return list(map(lambda element:
                    {'접수번호': element['rcept_no'],
                     '법인구분': element['corp_cls'],
                     '고유번호': element['corp_code'],
                     '회사명': element['corp_name'],
                     '법인명': element['inv_prm'],
                     '최초 취득 일자': element['frst_acqs_de'],
                     '출자 목적': element['invstmnt_purps'],
                     '최초 취득 금액': element['frst_acqs_amount'],
                     '기초 잔액 수량': element['bsis_blce_qy'],
                     '기초 잔액 지분 율': element['bsis_blce_qota_rt'],
                     '기초 잔액 장부 가액': element['bsis_blce_acntbk_amount'],
                     '증가 감소 취득 처분 수량': element['incrs_dcrs_acqs_dsps_qy'],
                     '증가 감소 취득 처분 금액': element['incrs_dcrs_acqs_dsps_amount'],
                     '증가 감소 평가 손액': element['incrs_dcrs_evl_lstmn'],
                     '기말 잔액 수량': element['trmend_blce_qy'],
                     '기말 잔액 지분 율': element['trmend_blce_qota_rt'],
                     '기말 잔액 장부 가액': element['trmend_blce_acntbk_amount'],
                     '최근 사업 연도 재무 현황 총 자산': element['recent_bsns_year_fnnr_sttus_tot_assets'],
                     '최근 사업 연도 재무 현황 당기 순이익': element['recent_bsns_year_fnnr_sttus_thstrm_ntpf']}, response))

def marshall_datas(api, response):
    response = copied_list_of_dicts(response)
    with open('../api_info.json', 'r') as f:
        json_data = json.load(f)
    print(json.dumps(json_data[api]))


# 임원 현황
async def get_executives(row, year, quarter):
    response = await request_to_dart('exctvSttus.json', row, year, quarter)
    if response is None:
        return
    return marshall_executives(response['list'])

async def get_shareholders(row, year, quarter):
    response = await request_to_dart('hyslrSttus.json', row, year, quarter)
    if response is None:
        return
    return marshall_shareholders(response['list'])

async def get_invest_history(row, year, quarter):
    response = await request_to_dart('otrCprInvstmntSttus.json', row, year, quarter)
    if response is None:
        return
    return marshall_investment(response['list'])

def return_api(api):
    if api == '임원목록':
        return get_executives
    elif api == '최대주주현황':
        return get_shareholders
    elif api == '타법인출자현황':
        return get_invest_history
    else:
        raise Exception("Wrong api name")


async def crawl_one_2_many(api, csv_filename, year, quarter):
    func = return_api(api) 
    results = await iterate_csv(csv_filename, year, quarter, func)
    new_csv_filename = get_new_csv_filename(csv_filename, api, year, quarter)
    list_to_csv(results, new_csv_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api', type=str, help='임원목록, 최대주주현황, 타법인출자현황')
    parser.add_argument('--csv_filename', type=str, help='상장사 목록 csv')
    parser.add_argument('--year', type=str, help='년도')
    parser.add_argument('--quarter', type=str, help='분기(1,2,3,4)')

    args = parser.parse_args()
    import time
    a = time.time()
    asyncio.run(crawl_one_2_many(args.api, args.csv_filename, args.year, args.quarter))
    print(f"takes {time.time() - a}")