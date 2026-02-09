import os
import requests
import time
import uuid
import hmac
import hashlib
from dotenv import load_dotenv

load_dotenv()

SOLAPI_API_KEY = os.environ.get("SOLAPI_API_KEY")
SOLAPI_SECRET_KEY = os.environ.get("SOLAPI_SECRET_KEY")
SOLAPI_SENDER_NUMBER = os.environ.get("SOLAPI_SENDER_NUMBER")

def get_iso_datetime():
    utc_offset_sec = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    utc_offset_sec = -utc_offset_sec
    hours, minutes = divmod(utc_offset_sec, 3600)
    minutes = divmod(minutes, 60)[0]
    time_str = "{}{:02d}:{:02d}".format('+' if utc_offset_sec >= 0 else '-', abs(int(hours)), abs(int(minutes)))
    date_str = time.strftime('%Y-%m-%dT%H:%M:%S')
    return date_str + time_str

def get_signature(key, date_salt):
    return hmac.new(key.encode(), date_salt.encode(), hashlib.sha256).hexdigest()

def get_headers():
    date = get_iso_datetime()
    salt = str(uuid.uuid4().hex)
    signature = get_signature(SOLAPI_SECRET_KEY, date + salt)
    return {
        'Authorization': f'HMAC-SHA256 apiKey={SOLAPI_API_KEY}, date={date}, salt={salt}, signature={signature}',
        'Content-Type': 'application/json'
    }

def send_sms(to_number: str, text: str):
    if not SOLAPI_API_KEY or not SOLAPI_SECRET_KEY:
        print(f"[MOCK SEND] To: {to_number}, Content: {text}")
        return {"status": "mock_success", "messageId": "mock_id"}

    url = "https://api.solapi.com/messages/v4/send"
    payload = {
        "message": {
            "to": to_number,
            "from": SOLAPI_SENDER_NUMBER,
            "text": text
        }
    }

    try:
        res = requests.post(url, json=payload, headers=get_headers())
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return {"status": "error", "error": str(e)}
