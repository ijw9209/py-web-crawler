# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from datetime import datetime

# # 현재 날짜 및 시간 가져오기
# now = datetime.now().strftime("%Y%m%d_%H%M")

# # 크롤링할 URL
# url = 'https://www.khug.or.kr/jeonse/web/s07/s070102.jsp'

# # URL에 HTTP GET 요청 보내기
# response = requests.get(url)

# soup = BeautifulSoup(response.text, 'html.parser')

# # 페이지 수 파악하기 (HTML 구조에 맞게 수정 필요)
# # 예를 들어, 페이지 번호가 <span class="page-number">로 되어 있다면 해당 요소를 찾아서 마지막 페이지 번호를 파악
# page_numbers = soup.find_all('span', class_='num')  # 클래스명은 실제 웹사이트의 구조에 맞게 수정
# last_page = 26 #int(page_numbers[-1].text)  # 마지막 페이지 번호 추출

# # 전체 페이지 크롤링하기
# all_data = []

# for page in range(1, last_page + 1):
#     # 페이지 번호를 쿼리 파라미터로 추가하여 URL 수정 01 서울 07 경기
#     page_url = f"{url}?sbGugun=ALL&CMB_SIDO=01&cur_page={page}"
#     # page_url = f"{url}?sbGugun=ALL&CMB_SIDO=07&cur_page={page}"
#     response = requests.get(page_url)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # 테이블 찾기 (예시로 테이블 데이터를 크롤링한다고 가정)
#         table = soup.find('table')  # 실제 테이블을 찾는 HTML 구조에 맞게 수정
#         rows = table.find_all('tr')
        
#         # 각 행에서 데이터 추출
#         for row in rows:
#             cols = row.find_all('td')
#             if len(cols) > 0:  # 빈 배열을 필터링
#                 cols = [col.text.strip() for col in cols]  # 데이터 텍스트만 추출
#                 all_data.append(cols)  # 모든 데이터를 리스트에 추가
    
#     else:
#         print(f"페이지 {page} 요청 실패")


# # DataFrame으로 변환 (원하는 열 이름을 넣어주기)
# df = pd.DataFrame(all_data, columns=["번호", "공고일자", "청약 접수기간	", "시도", "시군구" ,"주소", "주택유형" , "전용면적(m2)" , "임대보증금액" ,"신청자수"])  # 실제 테이블에 맞는 열 이름으로 수정

# # 엑셀 파일로 저장
# # 파일 이름에 날짜와 시간 추가
# file_name = f'크롤링_데이터{now}.xlsx'
# df.to_excel(file_name, index=False, engine='openpyxl')
# print(f"엑셀 파일 저장 완료: {file_name}")

# # 전체 데이터 출력 (원하는 형식으로 처리)
# for data in all_data:
#     print(data)

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 현재 날짜 및 시간 가져오기
now = datetime.now().strftime("%Y%m%d_%H%M")

# 지역 코드 목록 (서울: 01, 경기: 07 등)
regions = {
    "서울": "01",
    "경기": "07"
}

# 크롤링할 기본 URL
base_url = "https://www.khug.or.kr/jeonse/web/s07/s070102.jsp"

# 지역별 크롤링 실행
for region_name, sido_code in regions.items():
    all_data = []  # 각 지역별 데이터를 저장할 리스트

    # 첫 번째 페이지 요청 (마지막 페이지 번호 찾기)
    first_page_url = f"{base_url}?sbGugun=ALL&CMB_SIDO={sido_code}&cur_page=1"
    response = requests.get(first_page_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # **🔹 "마지막 페이지" 버튼에서 페이지 번호 가져오기**
        last_page = 1  # 기본값 1
        last_page_btn = soup.find("a", class_="last")  # "마지막 페이지" 버튼 찾기

        if last_page_btn and "href" in last_page_btn.attrs:
            last_page_url = last_page_btn["href"]  # href 속성 값 가져오기
            last_page = int(last_page_url.split("cur_page=")[-1])  # cur_page 값 추출

        print(f"{region_name} 지역 크롤링 시작 (총 {last_page} 페이지)")

        # 전체 페이지 크롤링
        for page in range(1, last_page + 1):
            page_url = f"{base_url}?sbGugun=ALL&CMB_SIDO={sido_code}&cur_page={page}"
            response = requests.get(page_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table')

                if table:
                    rows = table.find_all('tr')

                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) > 0:
                            cols = [col.text.strip() for col in cols]
                            all_data.append(cols)
            else:
                print(f"{region_name} 지역 페이지 {page} 요청 실패")

    else:
        print(f"{region_name} 지역 첫 페이지 요청 실패")
        continue  # 다음 지역으로 넘어감

    # DataFrame으로 변환
    df = pd.DataFrame(all_data, columns=["번호", "공고일자", "청약 접수기간", "시도", "시군구", "주소", "주택유형", "전용면적(m2)", "임대보증금액", "신청자수"])

    # 파일 저장 (지역명 포함)
    file_name = f'크롤링_데이터_{region_name}_{now}.xlsx'
    df.to_excel(file_name, index=False, engine='openpyxl')

    print(f"{region_name} 지역 크롤링 완료! 엑셀 저장: {file_name}")

print("모든 지역 크롤링 완료!")
