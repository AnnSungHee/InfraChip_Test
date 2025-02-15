from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# 환경 변수 로드
load_dotenv()

# API 키 가져오기
API_KEY = os.getenv("AIR_KOREA_API_KEY")

# FastAPI 앱 생성
app = FastAPI()

# CORS 에러 해결
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue 애플리케이션만 허용
    allow_credentials=True,
    allow_methods=["GET"],  # GET 요청만 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 에어코리아 API URL
AIR_KOREA_URL = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"


@app.get("/air-quality")
async def get_air_quality(station_name: str = "종로구", data_term: str = "DAILY"):
    """"
    파라미터 설정
    dataTerm 기간동안 stationName에서 측정된 대기오염정보 최근 rumOfRows개의 데이터 returnType으로 가지고 오기
    """
    params = {
        # API 인증 키
        "serviceKey": API_KEY,
        # 반환 데이터 타입
        "returnType": "json",
        # 최근 10개 데이터 가지고 오기
        "numOfRows": 10,
        # 페이지 번호
        "pageNo": 1,
        # 측정소 명
        "stationName": station_name,
        # 데이터 기간
        "dataTerm": data_term,
        # API 버전 - 버전 1.3을 호출할 경우 : PM10, PM2.5 1시간 등급 자료가 포함된 결과 표출
        "ver": "1.3",
    }

    # 에어코리아 API 요청
    response = requests.get(AIR_KOREA_URL, params=params)

    # API 요청이 성공할 경우
    if response.status_code == 200:
        data = response.json()
        if "response" in data and "body" in data["response"]:
            items = data["response"]["body"]["items"]
            result = [
                {
                    # 측정 시간
                    "dataTime": item["dataTime"],
                    # 미세먼지
                    "pm10": int(item["pm10Value"]) if item["pm10Value"].isdigit() else None,
                    # 초미세먼지
                    "pm25": int(item["pm25Value"]) if item["pm25Value"].isdigit() else None,
                    # 대기오염 지수
                    "air_quality_index": int(item["khaiGrade"]) if item["khaiGrade"].isdigit() else None,
                    # 대기오염 지수를 상태로 변환
                    "status": classify_air_quality(int(item["khaiGrade"]) if item["khaiGrade"].isdigit() else None),
                }
                for item in items
            ]
            return result
        else:
            return {"error": "Invalid response format"}
    
    return {"error": "Failed to fetch data"}

# 대기질 상태를 텍스트로 변환하는 함수
def classify_air_quality(khai_grade):
    if khai_grade == 1:
        return "좋음"
    elif khai_grade == 2:
        return "보통"
    elif khai_grade == 3:
        return "나쁨"
    elif khai_grade == 4:
        return "매우 나쁨"
    else:
        return "정보 없음"