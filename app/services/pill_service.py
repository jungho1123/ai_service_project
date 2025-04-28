# app/services/pill_service.py

import urllib.parse, requests, os  # URL 인코딩, HTTP 요청, 운영체제 경로 처리를 위한 모듈 임포트
from sqlalchemy.orm import Session  # SQLAlchemy 세션 ORM 임포트
from app.core.config import get_settings  # 환경 설정 불러오기
from app.core.database import get_db  # 데이터베이스 세션 생성 함수 불러오기
from app.models.pill import Pill  # Pill ORM 모델 임포트

settings = get_settings()  # 환경 설정 인스턴스 생성
DEFAULT_IMG = "http://localhost:8000/static/default-pill.png"  # 기본 약 이미지 URL 설정
SERVICE_KEY_RAW = settings.API_SERVICE_KEY  # 환경변수에서 공공데이터 API 키 로드
SERVICE_KEY = urllib.parse.quote(SERVICE_KEY_RAW, safe="")  # URL 안전하게 인코딩

def _api_by_item_seq(item_seq: int) -> dict:  # item_seq를 사용해 공공데이터 API로 약 정보를 요청하는 함수
    url = ("http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
           f"?serviceKey={SERVICE_KEY}&itemSeq={item_seq}&type=json")
    r = requests.get(url, timeout=10)  # 10초 타임아웃으로 GET 요청
    r.raise_for_status()  # HTTP 오류 발생 시 예외 발생
    data = r.json().get("body", {}).get("items", [])  # 응답 JSON 중 body → items 추출
    return (data[0] | {"source": "api"}) if data else {}  # 첫 번째 아이템에 소스정보 추가하여 반환

def get_by_class_id(db: Session, class_id: str) -> dict|None:  # 로컬 데이터베이스에서 class_id로 약 정보 검색
    pill = db.query(Pill).filter(Pill.class_id == class_id).first()  # 첫 번째 일치 레코드 조회
    if pill:
        return {
            "dl_name": pill.dl_name,
            "dl_material": pill.dl_material,
            "dl_company": pill.dl_company,
            "di_company_mf": pill.di_company_mf,
            "di_class_no": pill.di_class_no,
            "di_etc_otc_code": pill.di_etc_otc_code,
            "di_edi_code": pill.di_edi_code,
            "item_seq": pill.item_seq,
            "img_key": pill.img_key or DEFAULT_IMG,  # 이미지 없으면 기본 이미지 반환
            "source": "fallback"
        }
    return None  # 검색 실패 시 None 반환

def search_by_name(name: str) -> list[dict] | dict:  # 이름으로 약 검색하는 함수
    url = ("http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
           f"?serviceKey={SERVICE_KEY}&itemName={urllib.parse.quote(name)}&type=json&numOfRows=10&pageNo=1")
    r = requests.get(url, timeout=10)  # 10초 타임아웃으로 GET 요청
    r.raise_for_status()
    items = r.json().get("body", {}).get("items", [])
    if not items:
        return {"message": "해당 이름으로 등록된 약이 없습니다."}  # 검색 결과가 없을 때 메시지 반환
    return [
        {
            "itemName": i["itemName"], "entpName": i["entpName"],
            "itemSeq": i["itemSeq"], "itemImage": i.get("itemImage") or DEFAULT_IMG,
            "source": "api"
        } for i in items
    ]

def resolve_pill_info(class_id: str, item_seq_map: dict[str,int]) -> dict:  # class_id를 통해 약 정보를 통합 조회하는 함수
    from fastapi import HTTPException  # FastAPI 예외 클래스 임포트 (지연 임포트)
    db = next(get_db())  # 데이터베이스 세션 생성
    try:
        if (item_seq := item_seq_map.get(class_id)):  # 매핑 테이블에서 item_seq 찾기
            api_data = _api_by_item_seq(item_seq)  # 공공 API에서 약 정보 조회
            if api_data:
                return api_data
        # 공공 API 실패 또는 매핑 실패 시, fallback DB 검색 시도
        if (fallback := get_by_class_id(db, class_id)):
            return fallback
    finally:
        db.close()  # 세션 닫기
    raise HTTPException(status_code=404, detail=f"'{class_id}' 약 정보를 찾을 수 없습니다.")  # 검색 실패 시 404 에러 발생
