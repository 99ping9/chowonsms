import os
import sys
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import pytz

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)
KST = pytz.timezone('Asia/Seoul')

async def clear_logs():
    print("--- Clearing Logs for Re-testing ---")
    
    # 1. Find Reservation
    res_query = supabase.table("reservations").select("id").ilike("guest_name", "%윤현구%").execute()
    if not res_query.data:
        print("No reservation found.")
        return

    res_ids = [r['id'] for r in res_query.data]
    print(f"Found Reservation IDs: {res_ids}")

    # 2. Delete logs for today
    today_str = datetime.now(KST).strftime("%Y-%m-%d")
    start = f"{today_str} 00:00:00"
    end = f"{today_str} 23:59:59"
    
    print(f"Deleting logs for {today_str}...")
    
    try:
        # Delete logs for these reservations within today
        # Note: multiple .in_() might work, or loop
        res = supabase.table("sms_logs").delete()\
            .in_("reservation_id", res_ids)\
            .gte("sent_at", start)\
            .lte("sent_at", end)\
            .execute()
            
        print(f"Deleted {len(res.data)} logs.")
        print("✅ Ready for re-testing!")
        
    except Exception as e:
        print(f"Error deleting logs: {e}")

if __name__ == "__main__":
    asyncio.run(clear_logs())
