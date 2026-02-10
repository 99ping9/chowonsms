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

    if template.apply_all:
        # 그룹 식별 로직
        group_prefix = ""
        if "초원고택" in acc_name:
            group_prefix = "초원고택"
        elif "초원별장" in acc_name:
            group_prefix = "초원별장"
        elif "초원브릿지" in acc_name:
            group_prefix = "초원브릿지"
            
        if group_prefix:
            # 같은 그룹 + 같은 트리거인 모든 템플릿 업데이트
            # like 쿼리가 supabase-py에서 ilike or like로 사용 가능
            # 여기서는 간단히 모든 템플릿 가져와서 필터링 업데이트 하거나, 
            # 쿼리로 해결. .like("accommodation_name", f"{group_prefix}%") 사용
            response = supabase.table("message_templates").update(update_payload)\
                .eq("trigger_type", trigger_type)\
                .ilike("accommodation_name", f"{group_prefix}%")\
                .execute()
            return response.data[0] if response.data else {}
            
    # 단일 업데이트 (또는 전체공용 원본 업데이트)
    response = supabase.table("message_templates").update(update_payload).eq("id", template_id).execute()
    
    # [NEW] 전체공용 템플릿 수정 시, 모든 숙소의 해당 트리거 템플릿 일괄 업데이트
    if acc_name == '전체공용':
        supabase.table("message_templates").update(update_payload)\
            .eq("trigger_type", trigger_type)\
            .neq("accommodation_name", "전체공용")\
            .execute()

    return response.data[0]
