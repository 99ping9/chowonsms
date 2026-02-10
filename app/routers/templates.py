from fastapi import APIRouter, HTTPException, Depends
from app.database import get_supabase
from app.models import MessageTemplateCreate
from supabase import Client

router = APIRouter(prefix="/templates", tags=["templates"])

@router.get("/", response_model=list[dict])
async def get_templates(supabase: Client = Depends(get_supabase)):
    response = supabase.table("message_templates").select("*").order("accommodation_name, trigger_type").execute()
    return response.data

from app.models import MessageTemplateUpdate

@router.put("/{template_id}", response_model=dict)
async def update_template(template_id: int, template: MessageTemplateUpdate, supabase: Client = Depends(get_supabase)):
    # 1. 대상 템플릿 정보 조회
    target = supabase.table("message_templates").select("*").eq("id", template_id).execute()
    if not target.data:
        raise HTTPException(status_code=404, detail="Template not found")
    
    target_data = target.data[0]
    acc_name = target_data['accommodation_name']
    trigger_type = target_data['trigger_type']
    
    update_payload = {
        "subject": template.subject,
        "content": template.content,
        "send_time": str(template.send_time)
    }

    # 단일 업데이트 (apply_all 로직 제거됨)
    response = supabase.table("message_templates").update(update_payload).eq("id", template_id).execute()


    return response.data[0]
