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

missing_accommodations = [
    '초원별장(정글)', '초원별장(시네)', '초원브릿지'
]

def add_missing_templates():
    print("Adding missing 'checkin_0901' templates...")
    data_to_insert = []
    
    for acc in missing_accommodations:
        data_to_insert.append({
            "accommodation_name": acc,
            "trigger_type": "checkin_0901",
            "send_time": "09:00:00",
            "content": f"안녕하세요 {acc}입니다. 주차안내 드립니다.\n\n[주차장 주소]\n(주소를 입력해주세요)\n* 자세한 안내사항을 수정해서 사용해주세요."
        })

    try:
        response = supabase.table("message_templates").upsert(
            data_to_insert, 
            on_conflict="accommodation_name, trigger_type"
        ).execute()
        print(f"Successfully added {len(data_to_insert)} templates.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_missing_templates()
