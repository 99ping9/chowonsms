import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found.")
    sys.exit(1)

supabase: Client = create_client(url, key)

common_templates = [
    {
        "accommodation_name": "전체공용",
        "trigger_type": "checkin_1900",
        "send_time": "19:00:00",
        "content": """저녁 식사는 맛있게 하셨나요?

불편한 점이나 필요한 물품이 있으시면 언제든 연락주세요.
편안한 저녁 되세요."""
    },
    {
        "accommodation_name": "전체공용",
        "trigger_type": "checkout_0900",
        "send_time": "09:00:00",
        "content": """편안한 밤 되셨나요? 11시 퇴실 안내드립니다.

[퇴실 체크리스트]
- 분리수거 부탁드립니다.
- 보일러 외출 모드 변경
- 짐 확인해주세요."""
    },
    {
        "accommodation_name": "전체공용",
        "trigger_type": "checkout_1700",
        "send_time": "17:00:00",
        "content": """조심히 돌아가셨나요?

소중한 추억이 되셨길 바랍니다.
후기를 남겨주시면 큰 힘이 됩니다! 감사합니다."""
    },
    {
        "accommodation_name": "전체공용",
        "trigger_type": "multinight_0900",
        "send_time": "09:00:00",
        "content": """불편하신 점은 없으신가요?

수건이 더 필요하시면 말씀해주세요. 남은 일정도 편안하게 보내시길 바랍니다."""
    },
    {
        "accommodation_name": "전체공용",
        "trigger_type": "checkin_0900",
        "send_time": "09:00:00",
        "content": """{name}님, 숙소근처 맛집 볼거리 보내드립니다!

[맛집안내]
- OO식당: 한정식 정갈함
- XX카페: 뷰맛집

[볼거리]
- 산책로 A코스"""
    }
]

def add_common_templates():
    print("Adding '전체공용' accommodation...")
    try:
        supabase.table("accommodations").upsert({"name": "전체공용"}).execute()
    except Exception as e:
        print(f"Error adding accommodation: {e}")

    print("Adding '전체공용' templates...")
    try:
        response = supabase.table("message_templates").upsert(
            common_templates, 
            on_conflict="accommodation_name, trigger_type"
        ).execute()
        print(f"Successfully added {len(common_templates)} common templates.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_common_templates()
