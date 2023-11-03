from bs4 import BeautifulSoup
import requests
import json

DART_URL = 'https://opendart.fss.or.kr'
    
def get_target_category_urls(grpcd) -> dict[str]:
    top_url = '/guide/main.do?apiGrpCd='

    response = requests.get(DART_URL + top_url + grpcd)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        api_url_dict = {}
        temp = soup.select('table.tb01>tbody>tr>td')
        for i, t in enumerate(temp):
            if i % 4 == 1:
                api_url_dict[t.text] = DART_URL + temp[i+2].find('a', class_='link')['href']
    else:
        raise Exception("status error")
    
    return api_url_dict


def get_target_api_urls(api):

    response = requests.get(target_urls[3])

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.select('div.head_tit>h3')[0].text

        target_tag = soup.find_all('div', class_='DGCont')

def get_request_url(soup): # 기본 정보
    temp_dict = {}
    for t in soup:
        if t.select('div.titleWrapToggle>h5')[0].text == '기본 정보':
            infos = t.select('div.contWrapToggle>table.tb02>tbody>tr')[0].text.strip().split('\n') # json 주소
            request_address = infos[1]
            data_type = infos[3]
            temp_dict[data_type] = request_address
    return temp_dict

def get_request_params(soup): # 요청 인자
    temp_dict = {}
    for t in soup:
        if t.select('div.titleWrapToggle>h5')[0].text == '요청 인자':
            request_params = t.select('div.contWrapToggle>div.listFull_area>table.tb02>tbody>tr>td')
            for i, param in enumerate(request_params):
                if i % 5 == 0:
                    temp_dict[param.text] = request_params[i+3].text.strip()
    return temp_dict

def get_api_response(soup): # 응답 결과
    for t in soup:
        if t.select('div.titleWrapToggle>h5')[0].text == '응답 결과':
            temp_dict = {}
            response = t.select('div.contWrapToggle>table.tb02>tbody>tr>td.tl')
            for i, res in enumerate(response):
                # 영어 변수명
                if i % 3 == 0:
                    temp_dict[res.text.strip()] = response[i+1].text.strip()

    return temp_dict


if __name__ == "__main__":
    grpcd_list = ['DS001', 'DS002', 'DS003', 'DS004', 'DS005', 'DS006']
    temp_dict = dict()

    for grpcd in grpcd_list:
        target_urls = get_target_category_urls(grpcd)
        for k, v in target_urls.items():
            response = requests.get(v)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = k
                print(title)
                target_tag = soup.find_all('div', class_='DGCont')

                request_url = get_request_url(target_tag)
                request_params = get_request_params(target_tag)
                response_params = get_api_response(target_tag)

                temp_dict[title] = {
                    'request_url': request_url,
                    'request_params': request_params,
                    'response_params': response_params
                }

    with open("../api_info.json", "a", encoding='utf-8') as f:
        json.dump(temp_dict, f, ensure_ascii=False, indent=4)
                
                # print(json.dumps(json_data))
        # print(grpcd, target_urls)


    # response = requests.get(target_urls['분할'])

    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     # title = soup.select('div.head_tit>h3')[0].text # ex. 주요사항보고서 주요정보

    #     target_tag = soup.find_all('div', class_='DGCont')
        
    #     print(get_request_url(target_tag))
    #     print(get_request_params(target_tag))
    #     print(get_api_response(target_tag))





        # for t in target_tag:
        #     if t.select('div.titleWrapToggle>h5')[0].text == '기본 정보':
        #         print("\n기본 정보")
        #         infos = t.select('div.contWrapToggle>table.tb02>tbody>tr')[0].text.strip().split('\n') # json 주소
        #         request_address = infos[1]
        #         data_type = infos[3]
        #         print(request_address, data_type)
        #     elif t.select('div.titleWrapToggle>h5')[0].text == '요청 인자':
        #         print("\n요청 인자")
        #         request_params = t.select('div.contWrapToggle>div.listFull_area>table.tb02>tbody>tr>td')
        #         for i, param in enumerate(request_params):
        #             if i % 5 == 0:
        #                 print(param.text)     
        #     elif t.select('div.titleWrapToggle>h5')[0].text == '응답 결과':
        #         print('\n응답 결과')
        #         response = t.select('div.contWrapToggle>table.tb02>tbody>tr>td.tl')
        #         for i, res in enumerate(response):
        #             # 영어 변수명
        #             if i % 3 == 0:
        #                 print(res.text.strip())
        #             # 한글 변수명
        #             elif i % 3 == 1:
        #                 print(res.text.strip())
        #                 print()
                # print(t.select('div.contWrapToggle>div.listFull_area>table.tb02>tbody>tr>td.tl'))
        
        # target_tag = soup.select('div.DGCont>div.contWrapToggle>table.tb02>tbody>tr>td.tl')
        # target_tag = soup.select('div.DGCont>div.contWrapToggle>div.listFull_area>table.tb02>tbody>tr>td.tl')
        # target_tag = soup.select('div.DGCont>div.titleWrapToggle>h5')
        # for t in target_tag:
        #     print(t)
        
