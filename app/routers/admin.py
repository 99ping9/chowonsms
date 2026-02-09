from fastapi import APIRouter, Request, Depends, HTTPException, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")

# 환경 변수에서 PIN 로드 (기본값 설정은 개발 편의상, 배포시는 필수)
ADMIN_PIN = os.environ.get("ADMIN_PIN", "0000")

@router.get("/", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@router.post("/verify-pin")
async def verify_pin(payload: dict = Body(...)):
    input_pin = payload.get("pin")
    if input_pin == ADMIN_PIN:
        return JSONResponse(content={"status": "ok"})
    else:
        return JSONResponse(content={"status": "error", "message": "Invalid PIN"}, status_code=401)
