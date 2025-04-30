# app/api/pill_info.py
from fastapi import APIRouter, Query
from app.services import pill_service
from app.core.mappings import get_classid_to_itemseq

router = APIRouter(prefix="/pill-info", tags=["Pill"]) # APIRouter 객체 생성, '/pill-info' 경로에 대한 라우터 등록
CID2SEQ = get_classid_to_itemseq() # class_id를 item_seq로 변환하는 매핑 데이터를 메모리에 로딩

@router.get("")
def pill_info(class_id: str = Query(...)): # 전달받은 class_id를 이용해 약품 정보를 조회하고 반환
    return pill_service.resolve_pill_info(class_id, CID2SEQ)
