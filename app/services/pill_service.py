# app/services/pill_service.py

import urllib.parse, requests, os
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.models.pill import Pill

settings = get_settings()
DEFAULT_IMG = "http://localhost:8000/static/default-pill.png"
# API 키는 인코딩되지 않은 상태로 환경변수에서 가져오거나 기본값 사용
SERVICE_KEY_RAW = settings.API_SERVICE_KEY
# 한 번만 URL 인코딩 적용
SERVICE_KEY = urllib.parse.quote(SERVICE_KEY_RAW, safe="")

def _api_by_item_seq(item_seq: int) -> dict:
    url = (f"http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
           f"?serviceKey={SERVICE_KEY}&itemSeq={item_seq}&type=json")
    print(f"_api_by_item_seq URL: {url}")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
        print(f"Response status: {r.status_code}, text: {r.text[:500]}")
        data = r.json().get("body", {}).get("items", [])
        return (data[0] | {"source": "api"}) if data else {}
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {}
    except ValueError as e:
        print(f"JSON decode error: {e}, Response text: {r.text}")
        return {}

def get_by_class_id(db: Session, class_id: str) -> dict | None:
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
    url = (f"http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
           f"?serviceKey={SERVICE_KEY}&itemName={urllib.parse.quote(name)}&type=json&numOfRows=10&pageNo=1")
    print(f"Request URL: {url}")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
        print(f"Response status: {r.status_code}, encoding: {r.encoding}")
        print(f"Response text: {r.text[:500]}")
        
        try:
            items = r.json().get("body", {}).get("items", [])
        except ValueError as e:
            print(f"JSON decode error: {e}, Response text: {r.text}")
            return {"message": "API 응답을 파싱할 수 없습니다.", "error": str(e)}
        
        if not items:
            return {"message": "해당 이름으로 등록된 약이 없습니다."}
        
        return [
            {
                "itemName": item.get("itemName"),
                "entpName": item.get("entpName"),
                "efcyQesitm": item.get("efcyQesitm"),
                "useMethodQesitm": item.get("useMethodQesitm"),
                "atpnQesitm": item.get("atpnQesitm"),
                "atpnWarnQesitm": item.get("atpnWarnQesitm"),
                "intrcQesitm": item.get("intrcQesitm"),
                "seQesitm": item.get("seQesitm"),
                "depositMethodQesitm": item.get("depositMethodQesitm"),
                "itemSeq": item.get("itemSeq"),
                "itemImage": item.get("itemImage") or DEFAULT_IMG,
                "bizrno": item.get("bizrno"),
                "source": "api"
            } for item in items
        ]
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {"message": "API 요청 중 오류가 발생했습니다.", "error": str(e)}

def resolve_pill_info(class_id: str, item_seq_map: dict[str,int]) -> dict:
    from fastapi import HTTPException
    db = next(get_db())
    try:
        if (item_seq := item_seq_map.get(class_id)):
            api_data = _api_by_item_seq(item_seq)
            if api_data:
                return api_data
        if (fallback := get_by_class_id(db, class_id)):
            return fallback
    finally:
        db.close()
    raise HTTPException(status_code=404, detail=f"'{class_id}' 약 정보를 찾을 수 없습니다.")