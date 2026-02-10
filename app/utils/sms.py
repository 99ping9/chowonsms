import os
import requests
import uuid
import hmac
import hashlib
import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

SOLAPI_API_KEY = os.environ.get("SOLAPI_API_KEY")
SOLAPI_SECRET_KEY = os.environ.get("SOLAPI_SECRET_KEY")
SOLAPI_SENDER_NUMBER = os.environ.get("SOLAPI_SENDER_NUMBER")

# 1. 날짜 구하는 함수 (최신 방식으로 개선)
def get_iso_datetime():
    # 현재 시간을 구해서 ISO 8601 형식(표준 시간대 포함)으로 반환
    return datetime.datetime.now().astimezone().isoformat()

# 2. 서명(Signature) 생성 함수
def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

# 3. 헤더 생성 함수 (인증 정보 만들기)
def get_headers():
    date = get_iso_datetime()
    salt = str(uuid.uuid4().hex)
    combined_string = date + salt
    
    signature = get_signature(SOLAPI_SECRET_KEY, combined_string)
    
    return {
        'Authorization': f'HMAC-SHA256 apiKey={SOLAPI_API_KEY}, date={date}, salt={salt}, signature={signature}',
        'Content-Type': 'application/json'
    }

# 4. 문자 발송 함수
def send_sms(to_number: str, text: str, subject: str = None):
    # API 키가 없는 경우 (로컬 테스트 중 실수 방지)
    if not SOLAPI_API_KEY or not SOLAPI_SECRET_KEY:
        print(f"[MOCK SEND] To: {to_number}, Subject: {subject}, Content: {text}")
        return {"status": "mock_success", "messageId": "mock_id"}

    url = "https://api.solapi.com/messages/v4/send"
    
    # [안전장치] 전화번호에서 하이픈(-) 제거
    clean_number = to_number.replace("-", "").strip()

    message_payload = {
        "to": clean_number,
        "from": SOLAPI_SENDER_NUMBER,
        "text": text
    }

    if subject:
        message_payload["subject"] = subject

    payload = {
        "message": message_payload
    }

    try:
        # 헤더를 매 요청마다 새로 생성해야 함 (시간 정보 때문)
        res = requests.post(url, json=payload, headers=get_headers())
        res.raise_for_status() # 200 OK가 아니면 에러 발생시킴
        
        # 성공 시 결과 반환
        return res.json()
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        print(f"Response Body: {res.text}") # 에러 원인(API 응답) 출력
        return {"status": "error", "error": str(err), "detail": res.text}
        
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return {"status": "error", "error": str(e)}