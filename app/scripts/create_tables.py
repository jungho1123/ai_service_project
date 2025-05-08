# app/scripts/create_tables.py

from app.core.database import Base, engine  # 데이터베이스 Base 클래스와 엔진 객체 임포트
from app.models.pill import Pill  # Pill 테이블 ORM 모델 임포트
from app.models.alarm import Alarm
from app.models.user import User
def init_db():  # 데이터베이스 테이블을 생성하는 함수 정의
    print("  Creating tables")  # 테이블 생성 시작 로그 출력
    Base.metadata.create_all(bind=engine)  # Base 클래스에 등록된 모든 테이블을 데이터베이스에 생성
    print("  Done.")  # 테이블 생성 완료 로그 출력

if __name__ == "__main__":
    init_db()