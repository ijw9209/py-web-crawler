import requests
import json

def get_public_data(service_key, url, params=None):
    """
    공공 데이터 포털 Open API에서 데이터를 가져오는 함수
    :param service_key: 공공 데이터 포털에서 발급받은 서비스 키
    :param url: 요청할 API 엔드포인트
    :param params: 추가적으로 필요한 요청 파라미터 (dict 형태)
    :return: API 응답 JSON 데이터
    """
    headers = {"Content-Type": "application/json"}
    
    # 기본 파라미터에 서비스 키 추가
    if params is None:
        params = {}
    params["serviceKey"] = service_key
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    SERVICE_KEY = "" #YOUR_SERVICE_KEY  # 여기에 발급받은 서비스 키 입력
    API_URL = "https://api.odcloud.kr/api/15139525/v1/uddi:5b6bf851-162c-4927-9783-b4a391488c8d?page=1&perPage=1000"  # 실제 사용할 API 엔드포인트 입력
    
    # 필요한 파라미터 설정
    query_params = {
        "type": "json",
        "page": 1,
        "perPage": 10
    }
    
    data = get_public_data(SERVICE_KEY, API_URL, query_params)
    
    if data:
        print(json.dumps(data, indent=4, ensure_ascii=False))
