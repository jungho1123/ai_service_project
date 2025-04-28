# app/models/pill.py

from sqlalchemy import Column, Integer, String  # SQLAlchemy ORM 컬럼 타입 임포트
from app.core.database import Base  # SQLAlchemy Base 클래스 임포트

class Pill(Base):  # Pill 테이블의 ORM 모델 클래스 정의
    __tablename__ = "pills"  # 데이터베이스에서 사용될 테이블 이름 설정

    id = Column(Integer, primary_key=True, index=True)  # 기본 키로 사용되는 id 컬럼, 인덱스 생성
    class_id = Column(String, unique=True, nullable=False, index=True)  # 약품 고유 식별자, 유니크 제약 및 인덱스 적용
    dl_name = Column(String)  # 약품 이름
    dl_material = Column(String)  # 주요 성분 정보
    dl_company = Column(String)  # 제조사 이름
    di_company_mf = Column(String)  # 제조업체명 (추가 정보)
    di_class_no = Column(String)  # 분류 번호
    di_etc_otc_code = Column(String)  # 일반의약품/전문의약품 구분 코드
    di_edi_code = Column(String)  # 보험 청구용 EDI 코드
    item_seq = Column(Integer)  # 공공데이터 포털 itemSeq
    img_key = Column(String)  # 약 이미지 파일명 또는 키