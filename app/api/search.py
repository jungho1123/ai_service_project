# app/api/search.py
from fastapi import APIRouter, Query
from app.services import pill_service
router = APIRouter(prefix="/search", tags=["Search"])

@router.get("")
def search(name: str = Query(...)):
    return pill_service.search_by_name(name)
