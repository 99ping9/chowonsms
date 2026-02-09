from fastapi import APIRouter, Depends, HTTPException
from app.database import get_supabase
from app.utils.sms import send_sms
from datetime import datetime
import pytz
from supabase import Client
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/sms", tags=["sms"])
admin_router = APIRouter(prefix="/admin", tags=["admin"])

KST = pytz.timezone('Asia/Seoul')

class ManualSendRequest(BaseModel):
    reservation_id: int
    template_type: str # 'checkin', 'checkout', 'custom', 'common'
    custom_content: Optional[str] = None
    template_id: Optional[int] = None

@router.post("/send-manual")
async def send_manual_sms(req: ManualSendRequest, supabase: Client = Depends(get_supabase)):
    # 1. 예약 정보 가져오기
    res_data = supabase.table("reservations").select("*").eq("id", req.reservation_id).single().execute()
    if not res_data.data:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    reservation = res_data.data
    
    # 2. 메시지 내용 결정
    content = ""
    if req.custom_content:
        content = req.custom_content
    elif req.template_type == 'common':
         # Fetch 'common' template from DB
         tmpl_res = supabase.table("message_templates").select("*").eq("trigger_type", "common").execute()
         if tmpl_res.data:
             content = tmpl_res.data[0]['content']
         else:
             # Fallback or Error
             content = "[공지사항] {name}님, 초원SMS에서 알려드립니다.\n\n(관리자 페이지에서 공통 템플릿 내용을 설정해주세요.)" 
    else:
        # DB에서 적절한 템플릿 찾기
        # trigger_type이 req.template_type을 포함하고, accommodation_name이 일치하거나 'all'인 것
        # 정확한 매칭을 위해선 template_id를 받는게 가장 확실함
        
        if req.template_id:
            tmpl_res = supabase.table("message_templates").select("*").eq("id", req.template_id).single().execute()
            if tmpl_res.data:
                content = tmpl_res.data['content']
            else:
                raise HTTPException(status_code=404, detail="Template not found")
        else:
            # Fallback: 타입과 숙소명으로 검색
            # 예: trigger_type like '%checkin%'
            pass

    if not content:
        raise HTTPException(status_code=400, detail="Content could not be determined")

    # 3. 변수 치환
    formatted_content = content.format(
        name=reservation['guest_name'],
        accommodation=reservation['accommodation_name']
    )

    # 4. 발송
    send_result = send_sms(reservation['phone_number'], formatted_content)
    
    # 5. 로그 기록
    status = 'success'
    if isinstance(send_result, dict) and ('error' in send_result or send_result.get('status') == 'error'):
        status = 'failed'

    now_kst = datetime.now(KST)
    log_data = {
        "reservation_id": reservation['id'],
        "trigger_type": "manual_" + req.template_type,
        "sent_at": str(now_kst),
        "sent_date": str(now_kst.date()),
        "status": status,
        # "content": formatted_content # 로그 테이블에 content 컬럼이 있다면 추가
    }
    
    try:
        supabase.table("sms_logs").insert(log_data).execute()
    except Exception as e:
        print(f"Log insert failed: {e}")

    if status == 'failed':
         raise HTTPException(status_code=500, detail=f"SMS Sending Failed: {send_result.get('error')}")

    return {"status": "success", "result": send_result}

@router.get("/logs")
async def get_sms_logs(supabase: Client = Depends(get_supabase)):
    # 로그와 예약 정보를 조인해서 가져와야 함.
    # Supabase JS client는 조인이 쉽지만, Python client는 raw query나 rpc를 쓰거나, 두 번 쿼리해야 함.
    # 여기서는 간단히 두 번 쿼리해서 병합 (데이터 양이 적을 때 유효)
    
    logs_res = supabase.table("sms_logs").select("*").order("sent_at", desc=True).limit(50).execute()
    logs = logs_res.data
    
    if not logs:
        return []

    # 관련된 reservation_id 추출
    res_ids = [log['reservation_id'] for log in logs]
    
    # 예약 정보 조회
    reservations_res = supabase.table("reservations").select("id, guest_name, accommodation_name, phone_number").in_("id", res_ids).execute()
    reservations = {r['id']: r for r in reservations_res.data}
    
    # 병합
    result = []
    for log in logs:
        res_info = reservations.get(log['reservation_id'], {})
        result.append({
            **log,
            "guest_name": res_info.get("guest_name", "Unknown"),
            "accommodation_name": res_info.get("accommodation_name", "-"),
            "phone_number": res_info.get("phone_number", "-")
        })
        
    return result
