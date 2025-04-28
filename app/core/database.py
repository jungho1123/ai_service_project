# app/core/database.py

from sqlalchemy import create_engine  # SQLAlchemy 데이터베이스 엔진 생성 함수 임포트
from sqlalchemy.orm import sessionmaker, declarative_base  # 세션 팩토리와 베이스 클래스 생성 함수 임포트
from app.core.config import get_settings  # 환경변수 설정을 불러오는 함수 임포트

settings = get_settings()  # 환경변수에서 설정값을 로드하여 settings 인스턴스 생성
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)  # 데이터베이스 연결 엔진 생성, 연결 체크 활성화
SessionLocal = sessionmaker(bind=engine, autoflush=False)  # 엔진에 바인딩된 세션 팩토리 생성, 자동 플러시 비활성화
Base = declarative_base()  # ORM 모델 정의를 위한 베이스 클래스 생성

def get_db():  # 요청마다 사용할 데이터베이스 세션을 생성하는 의존성 함수 정의
    db = SessionLocal()  # 새로운 데이터베이스 세션 인스턴스 생성
    try:
        yield db  # 세션을 호출자에게 제공
    finally:
        db.close()  # 요청 처리 후 세션을 안전하게 종료
