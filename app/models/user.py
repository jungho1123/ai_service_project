# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime  # SQLAlchemy 컬럼 타입
from datetime import datetime  # datetime 기본 모듈
from zoneinfo import ZoneInfo  # Python 3.9+ 타임존 처리 모듈
from app.core.database import Base  # 공통 Base 클래스

# 현재 한국 시간 반환 함수
def kr_now():
    return datetime.now(ZoneInfo("Asia/Seoul"))

class User(Base):
    __tablename__ = "users"  # 사용자 테이블명

    id = Column(Integer, primary_key=True, index=True)  # 사용자 고유 ID
    email = Column(String, unique=True, nullable=False, index=True)  # 이메일 (로그인 ID)
    hashed_password = Column(String, nullable=False)  # 암호화된 비밀번호
    name = Column(String)  # 사용자 이름
    created_at = Column(DateTime(timezone=True), default=kr_now)  # 생성 시각 (한국시간 기준)