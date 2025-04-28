# app/main.py

from fastapi import FastAPI  # FastAPI 메인 서버 클래스 임포트
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어 임포트
from fastapi.staticfiles import StaticFiles  # 정적 파일 제공을 위한 StaticFiles 모듈 임포트
from fastapi.responses import JSONResponse  # JSON 응답 객체 임포트
from fastapi.exceptions import RequestValidationError  # 요청 검증 에러 핸들링을 위한 예외 클래스 임포트
from starlette.exceptions import HTTPException as StarletteHTTPException  # HTTP 예외 핸들링을 위한 Starlette 예외 클래스 임포트

from app.core.config import get_settings  # 환경 설정 가져오기
from app.api import predict, pill_info, search  # API 라우터 모듈 가져오기

settings = get_settings()  # 설정 인스턴스 생성
app = FastAPI(title="Pill-Info Service")  # FastAPI 앱 인스턴스 생성 및 제목 설정

# ────────────────────────────── CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # 허용할 Origin 목록
    allow_credentials=True,  # 인증 정보 허용 여부
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# ────────────────────────────── 정적 파일 경로 마운트
app.mount("/static", StaticFiles(directory="app/static"), name="static")  # '/static' URL로 정적 파일 제공

# ────────────────────────────── API 라우터 등록
for r in (predict.router, pill_info.router, search.router):
    app.include_router(r)  # 각각의 라우터를 FastAPI 앱에 포함

# ────────────────────────────── 글로벌 에러 핸들러 등록
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):  # HTTP 예외 발생 시 핸들링
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):  # 요청 검증 실패 시 핸들링
    return JSONResponse({"detail": exc.errors()}, status_code=422)