import os
import pytz
from datetime import datetime, timedelta, time
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_supabase
from app.utils.sms import send_sms
from supabase import Client

router = APIRouter(prefix="/api", tags=["cron"])

# Strict Timezone Enforce
KST = pytz.timezone('Asia/Seoul')

@router.get("/cron")
async def cron_job(manual_time: str = None, manual_date: str = None, supabase: Client = Depends(get_supabase)):
    # 1. 현재 시간 (KST) 구하기
    now_kst = datetime.now(KST)
    
    # [Customer Request] Manual Date for Testing (YYYY-MM-DD)
    if manual_date:
        try:
            target_date = datetime.strptime(manual_date, "%Y-%m-%d").date()
            now_kst = now_kst.replace(year=target_date.year, month=target_date.month, day=target_date.day)
            print(f"[TEST] Manual Date used: {manual_date}")
        except ValueError:
             return {"status": "error", "message": "Invalid manual_date format. Use YYYY-MM-DD"}

    # [Customer Request] Manual Time for Testing (HH:MM)
    if manual_time:
        try:
            h, m = map(int, manual_time.split(':'))
            now_kst = now_kst.replace(hour=h, minute=m, second=0, microsecond=0)
            print(f"[TEST] Manual Time used: {manual_time}")
        except ValueError:
            return {"status": "error", "message": "Invalid manual_time format. Use HH:MM"}

    current_time_str = now_kst.strftime("%H:%M") # "09:00" 분 단위까지만
    today_date = now_kst.date()
    
    # 2. 템플릿 가져오기 (전체 로드 - 데이터 크기 작음)
    templates_res = supabase.table("message_templates").select("*").execute()
    templates = templates_res.data
    
    # 3. '활성 예약' 가져오기 (입실일 <= 오늘 <= 퇴실일)
    # Supabase 쿼리 제한으로 인해 범위로 넉넉히 가져와서 코드 레벨 필터링이 안전할 수 있음
    # 하지만 여기선 lte/gte 로 최대한 필터링
    active_reservations_res = supabase.table("reservations").select("*")\
        .lte("checkin_date", str(today_date))\
        .gte("checkout_date", str(today_date))\
        .execute()
        
    reservations = active_reservations_res.data
    
    processed_count = 0
    skipped_count = 0

    for res in reservations:
        checkin_date = datetime.strptime(res['checkin_date'], '%Y-%m-%d').date()
        checkout_date = datetime.strptime(res['checkout_date'], '%Y-%m-%d').date()
        
        # 예약자별 적용 가능한 트리거 후보군 선정
        candidate_triggers = []
        
        # (1) 입실일 당일
        if checkin_date == today_date:
            candidate_triggers.extend([t for t in templates if 'checkin' in t['trigger_type']])
            
        # (2) 퇴실일 당일
        if checkout_date == today_date:
            candidate_triggers.extend([t for t in templates if 'checkout' in t['trigger_type']])
            
        # (3) 연박 (입실일 < 오늘 < 퇴실일)
        if checkin_date < today_date < checkout_date:
            candidate_triggers.extend([t for t in templates if 'multinight' in t['trigger_type']])
            
        # (4) 숙소 이름 일치 여부 필터링 (공통메세지 포함)
        # [Customer Request] '공통메세지'는 모든 숙소(초원고택1~3, 별장(시네/정글), 브릿지)에 적용됨
        res_accommodation = res['accommodation_name']
        candidate_triggers = [
            t for t in candidate_triggers 
            if t['accommodation_name'] == res_accommodation or t['accommodation_name'] == '공통메세지'
        ]
        
        # [NEW] 실행 순서 보장을 위해 정렬 (trigger_type 기준 오름차순)
        # checkin_0900 (맛집) -> checkin_0901 (체크인안내) 순서 보장됨
        candidate_triggers.sort(key=lambda x: x['trigger_type'])

        for tmpl in candidate_triggers:
            # 4. 시간 비교 (분 단위 일치 여부)
            # tmpl['send_time'] (e.g. "09:00:00")
            tmpl_hm = tmpl['send_time'][:5] # "09:00"
            
            if tmpl_hm == current_time_str:
                # 시간 일치! 중복 체크 및 발송 시도
                result = await process_sending(supabase, res, tmpl, now_kst)
                if result:
                    processed_count += 1
                else:
                    skipped_count += 1
            else:
                # 시간 불일치 - 패스
                continue

    return {
        "status": "ok", 
        "server_time_kst": str(now_kst), 
        "match_minute": current_time_str,
        "processed": processed_count,
        "skipped_duplicate": skipped_count
    }

async def process_sending(supabase, reservation, template, now_kst):
    """
    중복 발송 방지 및 실제 문자 발송 처리 검증
    """
    trigger_type = template['trigger_type']
    reservation_id = reservation['id']
    
    # [Critical] 중복 방지 체크
    # 조건: reservation_id AND trigger_type AND sent_at(오늘 날짜)
    today_start = now_kst.strftime("%Y-%m-%d 00:00:00")
    today_end = now_kst.strftime("%Y-%m-%d 23:59:59")
    
    # [Customer Request] 중복 발송 제한 해제 (2026-02-10)
    # check_log = supabase.table("sms_logs").select("id")\
    #     .eq("reservation_id", reservation_id)\
    #     .eq("trigger_type", trigger_type)\
    #     .gte("sent_at", today_start)\
    #     .lte("sent_at", today_end)\
    #     .execute()
        
    # if check_log.data and len(check_log.data) > 0:
    #     return False

    # 메시지 내용 포맷팅
    content = template['content'].format(
        name=reservation['guest_name'],
        accommodation=reservation['accommodation_name']
    )
    
    subject = template.get('subject') # [NEW] 템플릿에서 제목 가져오기
    formatted_subject = None
    if subject:
        try:
            formatted_subject = subject.format(
                name=reservation['guest_name'],
                accommodation=reservation['accommodation_name']
            )
        except Exception:
            formatted_subject = subject

    print(f"[SMS SENDING] To: {reservation['guest_name']}, Subject: {formatted_subject}, Msg: {content[:20]}...")
    
    # SMS 발송 (Mock 또는 Real)
    send_result = send_sms(reservation['phone_number'], content, subject=formatted_subject)
    
    # 성공 여부 판단
    status = 'success'
    if isinstance(send_result, dict) and ('error' in send_result or send_result.get('status') == 'error'):
        status = 'failed'
    
    # 로그 기록 (성공 여부 상관없이 시도했으면 기록하여 무한 재시도 방지 - 실패시 처리는 별도 정책 필요하지만 여기선 중복방지 우선)
    # 실패했더라도 재시도 로직이 없으면 'failed'로 남겨서 오늘 다시 안보내게 하는게 안전할 수 있음 (또는 status='failed'는 재시도 대상이 될 수도)
    # 요구사항: "중복 발송 절대 방지" -> 실패했어도 오늘 기록 남기는게 안전.
    
    # insert log
    log_data = {
        "reservation_id": reservation_id,
        "trigger_type": trigger_type,
        "sent_at": str(now_kst), 
        "sent_date": str(now_kst.date()), # [추가] DB Unique 제약조건 대응
        "status": status
    }
    
    try:
        supabase.table("sms_logs").insert(log_data).execute()
        return True
    except Exception as e:
        print(f"Error inserting log: {e}")
        return False
