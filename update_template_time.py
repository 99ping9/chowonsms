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

def update_time():
    print("Updating checkin_0901 send_time to 09:00:00...")
    try:
        # checkin_0901 트리거를 가진 모든 템플릿 업데이트
        response = supabase.table("message_templates").update({
            "send_time": "09:00:00"
        }).eq("trigger_type", "checkin_0901").execute()
        
        print("Update successful.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_time()
