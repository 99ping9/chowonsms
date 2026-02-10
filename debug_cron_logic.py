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

if not url or not key:
    print("Error: Missing SUPABASE_URL or SUPABASE_KEY")
    sys.exit(1)

supabase: Client = create_client(url, key)
KST = pytz.timezone('Asia/Seoul')

async def debug_cron():
    print("--- Debugging Cron Logic ---")
    
    # 1. Target Date: 2026-02-10 (As per user request)
    target_date_str = "2026-02-10"
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    target_time_str = "09:00"
    print(f"Target Date: {target_date}")
    print(f"Target Time: {target_time_str}")

    # 2. Fetch Reservation for '윤현구'
    print("\n[1] Searching for reservation '윤현구'...")
    res_query = supabase.table("reservations").select("*").ilike("guest_name", "%윤현구%").execute()
    reservations = res_query.data
    
    target_res = None
    if not reservations:
        print("❌ No reservation found for '윤현구'.")
    else:
        # Find the one covering Feb 10
        for r in reservations:
            checkin = datetime.strptime(r['checkin_date'], "%Y-%m-%d").date()
            checkout = datetime.strptime(r['checkout_date'], "%Y-%m-%d").date()
            print(f"  - Found: {r['guest_name']} ({r['accommodation_name']}): {checkin} ~ {checkout}")
            
            if checkin < target_date < checkout:
                print("    ✅ This is a MULTI-NIGHT stay on Feb 10.")
                target_res = r
            elif checkin == target_date:
                print("    ℹ️ This is CHECK-IN day.")
            elif checkout == target_date:
                print("    ℹ️ This is CHECK-OUT day.")
            else:
                print("    ℹ️ Not active on Feb 10.")

    if not target_res:
        print("❌ Could not find a multi-night reservation for '윤현구' on Feb 10.")
        return

    # 3. Fetch Templates
    print("\n[2] Fetching Multi-night Templates...")
    tmpl_query = supabase.table("message_templates").select("*").ilike("trigger_type", "%multinight%").execute()
    templates = tmpl_query.data
    
    matched_templates = []
    for t in templates:
        print(f"  - Template: {t['trigger_type']} (Time: {t['send_time']}, Acc: {t['accommodation_name']})")
        
        # Check logic
        if t['accommodation_name'] == target_res['accommodation_name'] or t['accommodation_name'] == '공통메세지':
            # Check time
            if t['send_time'].startswith(target_time_str):
                matched_templates.append(t)
                print("    ✅ MATCHES logic!")
            else:
                print(f"    ❌ Time mismatch (Expected {target_time_str})")
        else:
             print(f"    ❌ Accommodation mismatch (Res: {target_res['accommodation_name']})")

    if not matched_templates:
        print("❌ No matching templates found for this reservation at 09:00.")

    # 4. Check Logs (Did it already run?)
    print(f"\n[3] Checking Logs for Reservation ID {target_res['id']} on {target_date}...")
    
    # We need to check the whole day because the code checks 00:00:00 to 23:59:59
    day_start = f"{target_date_str} 00:00:00"
    day_end = f"{target_date_str} 23:59:59"
    
    logs = supabase.table("sms_logs").select("*")\
        .eq("reservation_id", target_res['id'])\
        .gte("sent_at", day_start)\
        .lte("sent_at", day_end)\
        .execute()
        
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        f.write("--- Templates ---\n")
        tmpls = supabase.table("message_templates").select("*").ilike("trigger_type", "%multinight%").execute()
        for t in tmpls.data:
            f.write(f"Template: {t['trigger_type']} | Time: {t['send_time']} | Acc: {t['accommodation_name']}\n")
        f.write("-" * 20 + "\n")

        if logs.data:
            f.write(f"⚠️ Logs found! Count: {len(logs.data)}\n")
            for log in logs.data:
                f.write(f"  - [LOG] ID: {log['id']}, Trigger: {log['trigger_type']}, Status: {log['status']}, Time: {log['sent_at']}\n")
        else:
            f.write("✅ No logs found for this reservation today. It SHOULD send if triggered.\n")

if __name__ == "__main__":
    asyncio.run(debug_cron())
