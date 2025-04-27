# app/services/pill_service.py
import urllib.parse, requests, os
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.models.pill import Pill

settings = get_settings()
DEFAULT_IMG = "http://localhost:8000/static/default-pill.png"
SERVICE_KEY_RAW = settings.API_SERVICE_KEY
SERVICE_KEY = urllib.parse.quote(SERVICE_KEY_RAW, safe="")

def _api_by_item_seq(item_seq: int) -> dict:
    url = ("http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
           f"?serviceKey={SERVICE_KEY}&itemSeq={item_seq}&type=json")
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json().get("body", {}).get("items", [])
    return (data[0] | {"source": "api"}) if data else {}

def get_by_class_id(db: Session, class_id: str) -> dict|None:
    pill = db.query(Pill).filter(Pill.class_id == class_id).first()
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
            "img_key": pill.img_key or DEFAULT_IMG,
            "source": "fallback"
        }
    return None

def search_by_name(name: str) -> list[dict] | dict:
    url = ("http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
           f"?serviceKey={SERVICE_KEY}&itemName={urllib.parse.quote(name)}&type=json&numOfRows=10&pageNo=1")
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    items = r.json().get("body", {}).get("items", [])
    if not items:
        return {"message": "해당 이름으로 등록된 약이 없습니다."}
    return [
        {
            "itemName": i["itemName"], "entpName": i["entpName"],
            "itemSeq": i["itemSeq"], "itemImage": i.get("itemImage") or DEFAULT_IMG,
            "source": "api"
        } for i in items
    ]

def resolve_pill_info(class_id: str, item_seq_map: dict[str,int]) -> dict:
    from fastapi import HTTPException
    db = next(get_db())  # FastAPI dep. 대체용 (스크립트 호출 시도 가능)
    try:
        if (item_seq := item_seq_map.get(class_id)):
            api_data = _api_by_item_seq(item_seq)
            if api_data:
                return api_data
        # API 실패 또는 미등록 → fallback
        if (fallback := get_by_class_id(db, class_id)):
            return fallback
    finally:
        db.close()
    raise HTTPException(status_code=404, detail=f"'{class_id}' 약 정보를 찾을 수 없습니다.")
