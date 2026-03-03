# Auto-generated backup of current DB templates
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase = create_client(url, key)

templates_data = [
    {
        'accommodation_name': '공통메세지',
        'trigger_type': 'checkin_1900',
        'send_time': '19:00:00',
        'subject': '저녁 안내',
        'content': '{name}님, 저녁 식사는 맛있게 하셨나요?...'
    },
    {
        'accommodation_name': '공통메세지',
        'trigger_type': 'checkin_food_0900',
        'send_time': '09:00:00',
        'subject': '맛집 안내',
        'content': '{name}님, 입실 전 주변 맛집을 소개해드립니다...'
    },
    {
        'accommodation_name': '공통메세지',
        'trigger_type': 'checkout_0900',
        'send_time': '09:00:00',
        'subject': '퇴실 안내',
        'content': '{name}님, 편안한 밤 되셨나요? 11시 퇴실입니다...'
    },
    {
        'accommodation_name': '공통메세지',
        'trigger_type': 'multinight_0900',
        'send_time': '09:00:00',
        'subject': '연박 안내',
        'content': '{name}님, 연박 안내드립니다...'
    },
    {
        'accommodation_name': '월명주택',
        'trigger_type': 'checkin_1450',
        'send_time': '14:50:00',
        'subject': '입실 안내',
        'content': '{name}님, 월명주택 입실 안내 내용입니다.\n\n'
    },
    {
        'accommodation_name': '월명주택',
        'trigger_type': 'checkin_guide_0900',
        'send_time': '09:00:00',
        'subject': '체크인 안내',
        'content': '{name}님, 월명주택 체크인 안내 내용입니다.\n\n'
    },
    {
        'accommodation_name': '월명주택',
        'trigger_type': 'checkout_1900',
        'send_time': '19:00:00',
        'subject': '후기 작성 요청',
        'content': '{name}님, 월명주택에서의 하루는 어떠셨나요? 소중한 후기를 남겨주세요. \n\n'
    },
    {
        'accommodation_name': '초원고택1',
        'trigger_type': 'checkin_1450',
        'send_time': '14:50:00',
        'subject': '입실 안내',
        'content': '{name}님, 초원고택1 입실 안내 내용입니다.\n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원고택1',
        'trigger_type': 'checkin_guide_0900',
        'send_time': '09:00:00',
        'subject': '체크인 안내',
        'content': '{name}님, 초원고택1 체크인 안내 내용입니다.\n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원고택1',
        'trigger_type': 'checkout_1900',
        'send_time': '19:00:00',
        'subject': '후기 작성 요청',
        'content': '{name}님, 초원고택1에서의 하루는 어떠셨나요? 소중한 후기를 남겨주세요. \n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원고택2',
        'trigger_type': 'checkin_1450',
        'send_time': '14:50:00',
        'subject': '입실 안내',
        'content': '{name}님, 초원고택2 입실 안내 내용입니다.\n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원고택2',
        'trigger_type': 'checkin_guide_0900',
        'send_time': '09:00:00',
        'subject': '체크인 안내',
        'content': '{name}님, 초원고택2 체크인 안내 내용입니다.\n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원고택2',
        'trigger_type': 'checkout_1900',
        'send_time': '19:00:00',
        'subject': '후기 작성 요청',
        'content': '{name}님, 초원고택2에서의 하루는 어떠셨나요? 소중한 후기를 남겨주세요. \n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원고택3',
        'trigger_type': 'checkin_1450',
        'send_time': '14:50:00',
        'subject': '입실 안내',
        'content': '{name}님, 초원고택3 입실 안내 내용입니다.\n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원고택3',
        'trigger_type': 'checkin_guide_0900',
        'send_time': '09:00:00',
        'subject': '체크인 안내',
        'content': '{name}님, 초원고택3 체크인 안내 내용입니다.\n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원고택3',
        'trigger_type': 'checkout_1900',
        'send_time': '19:00:00',
        'subject': '후기 작성 요청',
        'content': '{name}님, 초원고택3에서의 하루는 어떠셨나요? 소중한 후기를 남겨주세요. \n\n[초원고택 기본안내]'
    },
    {
        'accommodation_name': '초원별장(시네)',
        'trigger_type': 'checkin_1450',
        'send_time': '14:50:00',
        'subject': '입실 안내',
        'content': '{name}님, 초원별장(시네) 입실 안내 내용입니다.\n\n[초원별장 기본안내]'
    },
    {
        'accommodation_name': '초원별장(시네)',
        'trigger_type': 'checkin_guide_0900',
        'send_time': '09:00:00',
        'subject': '체크인 안내',
        'content': '{name}님, 초원별장(시네) 체크인 안내 내용입니다.\n\n[초원별장 기본안내]'
    },
    {
        'accommodation_name': '초원별장(시네)',
        'trigger_type': 'checkout_1900',
        'send_time': '19:00:00',
        'subject': '후기 작성 요청',
        'content': '{name}님, 초원별장(시네)에서의 하루는 어떠셨나요? 소중한 후기를 남겨주세요. \n\n[초원별장 기본안내]'
    },
    {
        'accommodation_name': '초원별장(정글)',
        'trigger_type': 'checkin_1450',
        'send_time': '14:50:00',
        'subject': '입실 안내',
        'content': '{name}님, 초원별장(정글) 입실 안내 내용입니다.\n\n[초원별장 기본안내]'
    },
    {
        'accommodation_name': '초원별장(정글)',
        'trigger_type': 'checkin_guide_0900',
        'send_time': '09:00:00',
        'subject': '체크인 안내',
        'content': '{name}님, 초원별장(정글) 체크인 안내 내용입니다.\n\n[초원별장 기본안내]'
    },
    {
        'accommodation_name': '초원별장(정글)',
        'trigger_type': 'checkout_1900',
        'send_time': '19:00:00',
        'subject': '후기 작성 요청',
        'content': '{name}님, 초원별장(정글)에서의 하루는 어떠셨나요? 소중한 후기를 남겨주세요. \n\n[초원별장 기본안내]'
    },
    {
        'accommodation_name': '초원브릿지',
        'trigger_type': 'checkin_1450',
        'send_time': '14:50:00',
        'subject': '입실 안내',
        'content': '{name}님, 초원브릿지 입실 안내 내용입니다.\n\n[초원브릿지 기본안내]'
    },
    {
        'accommodation_name': '초원브릿지',
        'trigger_type': 'checkin_guide_0900',
        'send_time': '09:00:00',
        'subject': '체크인 안내',
        'content': '{name}님, 초원브릿지 체크인 안내 내용입니다.\n\n[초원브릿지 기본안내]'
    },
    {
        'accommodation_name': '초원브릿지',
        'trigger_type': 'checkout_1900',
        'send_time': '19:00:00',
        'subject': '후기 작성 요청',
        'content': '{name}님, 초원브릿지에서의 하루는 어떠셨나요? 소중한 후기를 남겨주세요. \n\n[초원브릿지 기본안내]'
    },
]

def restore():
    print('Restoring templates from backup...')
    # Delete existing
    res = supabase.table('message_templates').select('id').execute()
    if res.data:
        ids = [r['id'] for r in res.data]
        supabase.table('message_templates').delete().in_('id', ids).execute()
    
    # Insert backups
    for t in templates_data:
        supabase.table('message_templates').insert(t).execute()
    print('Restore complete.')

if __name__ == '__main__':
    restore()
