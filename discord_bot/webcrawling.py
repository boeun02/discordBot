import requests
from bs4 import BeautifulSoup

def get_dju_notice_with_category(mi, bbsId, keyword):
    # URL 선택 및 저장
    base_url = "https://www.dju.ac.kr/dju/na/ntt/selectNttList.do"
    com_url = "https://www.dju.ac.kr/comeng2/na/ntt/selectNttList.do?mi=2241&bbsId=1354"
    selected_url = com_url if mi == '2241' and bbsId == '1354' else base_url


    url_params = {
        'mi': mi,
        'bbsId': bbsId,
        'searchCnd': '1',  # 0은 제목+내용, 1은 제목, 2는 내용, 3은 작성자
        'searchWrd': keyword
    }

    if keyword.strip() == "":
        url_params['searchCnd'] = '0'  # 제목+내용 모두 검색
    
    try:
        response = requests.get(base_url, params=url_params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            notice_items = soup.find('tbody').find_all('tr')
            
            notices = []
            for idx, item in enumerate(notice_items, start=1):
                notice_text = ' '.join(item.stripped_strings)
                notices.append(f"{idx}. {notice_text}")
            
            # 공지사항 링크 추가 (카테고리에 따라 다른 URL 사용)
            notices.append(f"\n자세한 내용은 여기에서 확인하세요: {'https://www.dju.ac.kr/dju/na/ntt/selectNttList.do?mi=1188&bbsId=1040'}")

            return '\n'.join(notices)
        else:
            return "HTTP 요청에 실패하였습니다."
    
    except Exception as e:
        return f"에러 발생: {e}"


# 새로 추가된 get_bus_info 함수
def get_bus_info(cntntsId, mi):
    bus_url = "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do"
    params = {
        'cntntsId': cntntsId,
        'mi': mi
    }

    try:
        response = requests.get(bus_url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 공지사항과 같은 방식으로 tbody의 tr 요소들을 순회합니다.
            bus_items = soup.find('tbody').find_all('tr')
            
            bus_notices = []
            for idx, item in enumerate(bus_items, start=1):
                notice_text = ' '.join(item.stripped_strings)
                bus_notices.append(f"{idx}. {notice_text}")
            
            # 시간표, 노선, 시내버스 정보에 대한 링크를 추가합니다.
            # 이 링크는 실제 요청을 처리하는 페이지를 반영해야 합니다.
            bus_notices.append(f"\n자세한 내용은 여기에서 확인하세요: {'https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=1828&mi=2954'}")

            return ' '.join(bus_notices)
        else:
            return "HTTP 요청에 실패하였습니다."

    except Exception as e:
        return f"에러 발생: {e}"
