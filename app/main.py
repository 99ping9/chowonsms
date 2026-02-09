from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import reservations, templates as templates_router, admin
from app.api import cron
import os

app = FastAPI(title="ChowonSMS", description="Automatic SMS System for accommodation reservation")

# Static files mount
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(reservations.router)
app.include_router(templates_router.router)
app.include_router(admin.router)
app.include_router(cron.router)
from app.routers import sms
app.include_router(sms.router)
app.include_router(sms.admin_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("reservations.html", {"request": request})
