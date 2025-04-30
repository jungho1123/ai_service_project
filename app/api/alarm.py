# app/api/alarm.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import time
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.alarm import Alarm
from app.models.user import User

router = APIRouter(prefix="/alarm", tags=["Alarm"])

# 알림 등록 요청 스키마
class AlarmCreate(BaseModel):
    class_id: str
    medicine_name: str
    dosage: str
    time: time
    repeat_days: str

@router.post("")
def create_alarm(payload: AlarmCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    alarm = Alarm(
        user_id=user.id,
        medicine_name=payload.medicine_name,
        dosage=payload.dosage,
        time=payload.time,
        repeat_days=payload.repeat_days
    )
    db.add(alarm)
    db.commit()
    return {"message": "복약 알림이 등록되었습니다."}

@router.get("")
def get_alarms(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    alarms = db.query(Alarm).filter(Alarm.user_id == user.id).all()
    return alarms