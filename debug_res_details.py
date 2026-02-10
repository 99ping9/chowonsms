import os
import sys
import asyncio
from datetime import datetime, date
from dotenv import load_dotenv
from supabase import create_client, Client
import pytz

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

async def debug_res():
    print("--- Reservation Details ---")
    res_query = supabase.table("reservations").select("*").ilike("guest_name", "%윤현구%").execute()
    
    with open("debug_res_output.txt", "w", encoding="utf-8") as f:
        if not res_query.data:
            f.write("No reservation found.\n")
            return

        for r in res_query.data:
            f.write(f"ID: {r['id']}\n")
            f.write(f"Accommodation: {r['accommodation_name']}\n")
            f.write(f"Check-in: {r['checkin_date']}\n")
            f.write(f"Check-out: {r['checkout_date']}\n")
            
            # Logs for this res
            logs = supabase.table("sms_logs").select("*").eq("reservation_id", r['id']).execute()
            f.write(f"Logs ({len(logs.data)}):\n")
            for log in logs.data:
                f.write(f"  - [SentAt: {log['sent_at']}] Trigger: {log['trigger_type']}, Status: {log['status']}\n")
            f.write("-" * 20 + "\n")

if __name__ == "__main__":
    asyncio.run(debug_res())
