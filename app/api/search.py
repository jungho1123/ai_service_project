# app/api/search.py
from fastapi import APIRouter, Query # APIRouter 객체 생성, '/search' 경로에 대한 라우터 등록
from app.services import pill_service # pill_service 모듈에서 약품 검색 기능 가져오기
router = APIRouter(prefix="/search", tags=["Search"]) # APIRouter 객체 생성, '/search' 경로에 대한 라우터 등록

@router.get("") # 검색어를 쿼리 파라미터로 받아 약품 정보를 조회하고 반환
def search(name: str = Query(...)): # name 쿼리 파라미터를 필수로 설정
    return pill_service.search_by_name(name) # 약품 이름으로 검색한 결과 반환
