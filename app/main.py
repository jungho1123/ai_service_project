# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.api import predict, pill_info, search

settings = get_settings()
app = FastAPI(title="Pill-Info Service")

# ────────────────────────────── CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────────── Static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ────────────────────────────── Routers
for r in (predict.router, pill_info.router, search.router):
    app.include_router(r)

# ────────────────────────────── Error Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({"detail": exc.errors()}, status_code=422)
