from pydantic import BaseModel
from datetime import date, datetime, time
from typing import Optional, List

class ReservationBase(BaseModel):
    guest_name: str
    phone_number: str
    accommodation_name: str
    checkin_date: date
    checkout_date: date
    memo: Optional[str] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MessageTemplateBase(BaseModel):
    accommodation_name: str
    trigger_type: str
    send_time: time
    subject: Optional[str] = None
    content: str
    
class MessageTemplateCreate(MessageTemplateBase):
    pass

class MessageTemplateUpdate(BaseModel):
    subject: Optional[str] = None
    content: str
    send_time: time
    apply_all: bool = False

class MessageTemplate(MessageTemplateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SMSLog(BaseModel):
    reservation_id: int
    trigger_type: str
    sent_at: datetime
    status: str
