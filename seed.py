import os
import sys
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

accommodations = [
    '초원고택1', '초원고택2', '초원고택3',
    '초원별장(정글)', '초원별장(시네)', '초원브릿지'
]

# 템플릿 데이터 정의
# {trigger: {time: "HH:MM:ss", content: "...", target: ["all" or list]}}
templates_data = {
    'checkin_0900': {
        'time': '09:00:00',
        'content': '{name}님, 숙소근처 맛집 볼거리 보내드립니다!\n\n[맛집안내]\n- OO식당: 한정식 정갈함\n- XX카페: 뷰맛집\n\n[볼거리]\n- 산책로 A코스\n...',
        'target': 'all'
    },
    'checkin_0901': {
        'time': '09:01:00',
        'content': '안녕하세요 초원고택입니다. 주차안내 드립니다.\n\n[주차장 주소]\n초원시 고택로 1길 1\n* 흰색 실선 안에 주차해주세요.',
        'target': ['초원고택1', '초원고택2', '초원고택3']
    },
    'checkin_1450': {
        'time': '14:50:00',
        'content': '안녕하세요! 오늘 3시 입실입니다.\n\n[비밀번호 및 유의사항]\n- 비밀번호: 1234*\n- 객실 내 금연\n- 와이파이: chowon / 12345678',
        'target': 'all'
    },
    'checkin_1900': {
        'time': '19:00:00',
        'content': '저녁 식사는 맛있게 하셨나요?\n\n불편한 점이나 필요한 물품이 있으시면 언제든 연락주세요.\n편안한 저녁 되세요.',
        'target': 'all'
    },
    'checkout_0900': {
        'time': '09:00:00',
        'content': '편안한 밤 되셨나요? 11시 퇴실 안내드립니다.\n\n[퇴실 체크리스트]\n- 분리수거 부탁드립니다.\n- 보일러 외출 모드 변경\n- 짐 확인해주세요.',
        'target': 'all'
    },
    'checkout_1700': {
        'time': '17:00:00',
        'content': '조심히 돌아가셨나요?\n\n소중한 추억이 되셨길 바랍니다.\n후기를 남겨주시면 큰 힘이 됩니다! 감사합니다.',
        'target': 'all'
    },
    'multinight_0900': {
        'time': '09:00:00',
        'content': '불편하신 점은 없으신가요?\n\n수건이 더 필요하시면 말씀해주세요. 남은 일정도 편안하게 보내시길 바랍니다.',
        'target': 'all'
    }
}

def seed_templates():
    print("Seeding message templates to Remote DB...")
    data_to_insert = []
    
    for acc in accommodations:
        for trigger, info in templates_data.items():
            # 타겟 필터링
            if info['target'] != 'all' and acc not in info['target']:
                continue
                
            data_to_insert.append({
                "accommodation_name": acc,
                "trigger_type": trigger,
                "send_time": info['time'],
                "content": info['content']
            })

    try:
        # upsert: accommodation_name + trigger_type 조합이 유니크하므로 충돌 시 업데이트되거나 무시됨
        # on_conflict 절이 동작하려면 해당 컬럼들에 UNIQUE 제약조건이 있어야 함 (schema.sql에 정의됨)
        response = supabase.table("message_templates").upsert(
            data_to_insert, 
            on_conflict="accommodation_name, trigger_type"
        ).execute()
        
        # response.data가 리스트 등으로 반환됨
        print(f"Successfully processed {len(data_to_insert)} templates.")
    except Exception as e:
        print(f"Error seeding templates: {e}")

if __name__ == "__main__":
    seed_templates()
