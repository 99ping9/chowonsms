import os
import sys
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv

# 로컬 테스트 시 .env 로드
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")
    print("Please check your .env file or Vercel environment variables.")
    sys.exit(1)

supabase: Client = create_client(url, key)

async def seed_templates():
    print("Seeding message templates (Refined Classification)...")
    
    # 1. Accommodations List
    rooms = [
        "초원고택1", "초원고택2", "초원고택3",
        "초원별장(시네)", "초원별장(정글)",
        "초원브릿지"
    ]
    
    # 2. Common Templates (공통메세지) - 5 items
    common_templates = [
        {
            "trigger_type": "checkin_food_0900", # 맛집안내
            "send_time": "09:00:00",
            "subject": "맛집 안내",
            "content": "{name}님, 입실 전 주변 맛집을 소개해드립니다..."
        },
        {
            "trigger_type": "checkin_1900", # 저녁안내
            "send_time": "19:00:00",
            "subject": "저녁 안내",
            "content": "{name}님, 저녁 식사는 맛있게 하셨나요?..."
        },
        {
            "trigger_type": "checkout_0900", # 퇴실안내
            "send_time": "09:00:00",
            "subject": "퇴실 안내",
            "content": "{name}님, 편안한 밤 되셨나요? 11시 퇴실입니다..."
        },
        {
            "trigger_type": "checkout_1700", # 리뷰요청
            "send_time": "17:00:00",
            "subject": "리뷰 요청",
            "content": "{name}님, 이용해주셔서 감사합니다. 리뷰 부탁드려요..."
        },
        {
            "trigger_type": "multinight_0900", # 연박안내
            "send_time": "09:00:00",
            "subject": "연박 안내",
            "content": "{name}님, 연박 안내드립니다..."
        }
    ]

    # 3. Specific Templates - 3 items per room
    specific_template_types = [
        {
            "trigger_type": "checkin_guide_0900", # 체크인안내 (기존 checkin_0900 대체)
            "send_time": "09:00:00",
            "subject": "체크인 안내"
        },
        {
            "trigger_type": "checkin_1450", # 입실안내
            "send_time": "14:50:00",
            "subject": "입실 안내"
        },
        {
            "trigger_type": "checkout_1900", # 후기작성요청 (NEW)
            "send_time": "19:00:00",
            "subject": "후기 작성 요청"
        }
    ]

    print("Clearing existing templates...")
    try:
        start_res = supabase.table("message_templates").select("id").execute()
        if start_res.data:
            ids = [r['id'] for r in start_res.data]
            supabase.table("message_templates").delete().in_("id", ids).execute()
    except Exception as e:
        print(f"Warning clearing templates: {e}")

    # Insert Common
    for t in common_templates:
        data = {
            "accommodation_name": "공통메세지", # Renamed from 공용메세지
            "trigger_type": t["trigger_type"],
            "send_time": t["send_time"],
            "subject": t["subject"],
            "content": t["content"]
        }
        supabase.table("message_templates").insert(data).execute()
        print(f"Inserted Common: {t['trigger_type']}")

    # Insert Specific
    for room in rooms:
        for t in specific_template_types:
            # Content generation based on room group
            group_suffix = ""
            if "초원고택" in room:
                group_suffix = "[초원고택 기본안내]"
            elif "초원별장" in room:
                group_suffix = "[초원별장 기본안내]"
            elif "초원브릿지" in room:
                group_suffix = "[초원브릿지 기본안내]"
            
            # Special content for checkout_1900
            if t['trigger_type'] == 'checkout_1900':
                 content = f"{{name}}님, {room}에서의 하루는 어떠셨나요? 소중한 후기를 남겨주세요. \n\n{group_suffix}"
            else:
                 content = f"{{name}}님, {room} {t['subject']} 내용입니다.\n\n{group_suffix}"
            
            data = {
                "accommodation_name": room,
                "trigger_type": t["trigger_type"],
                "send_time": t["send_time"],
                "subject": t["subject"],
                "content": content
            }
            supabase.table("message_templates").insert(data).execute()
        print(f"Inserted Specifics for: {room}")

    print("Seeding completed successfully.")


async def seed_groups():
    print("Seeding/Ensuring accommodation groups exist...")
    # List of all accommodation names used in templates
    groups = [
        "공통메세지",
        "초원고택1", "초원고택2", "초원고택3",
        "초원별장(시네)", "초원별장(정글)",
        "초원브릿지"
    ]
    
    data = [{"name": g} for g in groups]
    
    try:
        # Check existing to avoid constraint errors if using simple insert, or use upsert
        # Supabase upsert requires unique constraint on 'name'
        supabase.table("accommodations").upsert(data, on_conflict="name").execute()
        print("Groups seeded successfully.")
    except Exception as e:
        print(f"Error seeding groups: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_groups())
    asyncio.run(seed_templates())
