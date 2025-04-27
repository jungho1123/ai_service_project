# app/api/pill_info.py
from fastapi import APIRouter, Query
from app.services import pill_service
from app.core.mappings import get_classid_to_itemseq

router = APIRouter(prefix="/pill-info", tags=["Pill"])
CID2SEQ = get_classid_to_itemseq()

@router.get("")
def pill_info(class_id: str = Query(...)):
    return pill_service.resolve_pill_info(class_id, CID2SEQ)
