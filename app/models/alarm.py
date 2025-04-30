# app/models/alarm.py
from sqlalchemy import Column, Integer, String, Boolean, Time, DateTime, ForeignKey  # SQLAlchemy 컬럼 및 타입 정의
from sqlalchemy.orm import relationship  # 관계 설정을 위한 ORM 유틸
from datetime import datetime  # datetime 기본 모듈
from zoneinfo import ZoneInfo  # Python 3.9+에서 지원하는 타임존 처리 모듈
from app.core.database import Base  # 공통 Base 클래스
from app.models.user import User  # 분리된 사용자 모델 임포트

# 현재 한국 시간(Asia/Seoul) 반환 함수 (timezone-aware)
def kr_now():
    return datetime.now(ZoneInfo("Asia/Seoul"))

class Alarm(Base):
    __tablename__ = "alarms"  # 알림 테이블명 지정

    id = Column(Integer, primary_key=True, index=True)  # 알림 고유 ID
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 사용자 참조 ID
    medicine_name = Column(String, nullable=False)  # 약 이름
    dosage = Column(String)  # 복용량 (예: 1정)
    time = Column(Time, nullable=False)  # 복약 알림 시간
    repeat_days = Column(String)  # 반복 요일 문자열 (예: "월,화,수")
    is_active = Column(Boolean, default=True)  # 알림 활성 여부
    created_at = Column(DateTime(timezone=True), default=kr_now)  # 생성 일시 (한국 시간, timezone-aware)

    user = relationship("User", backref="alarms")  # 사용자-알림 간 관계 설정
