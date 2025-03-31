import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 현재 날짜 및 시간 가져오기
now = datetime.now().strftime("%Y%m%d_%H%M")

# 크롤링할 URL
url = 'https://www.khug.or.kr/jeonse/web/s07/s070102.jsp'

# URL에 HTTP GET 요청 보내기
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# 페이지 수 파악하기 (HTML 구조에 맞게 수정 필요)
# 예를 들어, 페이지 번호가 <span class="page-number">로 되어 있다면 해당 요소를 찾아서 마지막 페이지 번호를 파악
page_numbers = soup.find_all('span', class_='num')  # 클래스명은 실제 웹사이트의 구조에 맞게 수정
last_page = 26 #int(page_numbers[-1].text)  # 마지막 페이지 번호 추출

# 전체 페이지 크롤링하기
all_data = []

for page in range(1, last_page + 1):
    # 페이지 번호를 쿼리 파라미터로 추가하여 URL 수정
    page_url = f"{url}?sbGugun=ALL&CMB_SIDO=01&cur_page={page}"
    response = requests.get(page_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 테이블 찾기 (예시로 테이블 데이터를 크롤링한다고 가정)
        table = soup.find('table')  # 실제 테이블을 찾는 HTML 구조에 맞게 수정
        rows = table.find_all('tr')
        
        # 각 행에서 데이터 추출
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 0:  # 빈 배열을 필터링
                cols = [col.text.strip() for col in cols]  # 데이터 텍스트만 추출
                all_data.append(cols)  # 모든 데이터를 리스트에 추가
    
    else:
        print(f"페이지 {page} 요청 실패")


# DataFrame으로 변환 (원하는 열 이름을 넣어주기)
df = pd.DataFrame(all_data, columns=["번호", "공고일자", "청약 접수기간	", "시도", "시군구" ,"주소", "주택유형" , "전용면적(m2)" , "임대보증금액" ,"신청자수"])  # 실제 테이블에 맞는 열 이름으로 수정

# 엑셀 파일로 저장
# 파일 이름에 날짜와 시간 추가
file_name = f'크롤링_데이터_{now}.xlsx'
df.to_excel(file_name, index=False, engine='openpyxl')
print(f"엑셀 파일 저장 완료: {file_name}")

# 전체 데이터 출력 (원하는 형식으로 처리)
for data in all_data:
    print(data)