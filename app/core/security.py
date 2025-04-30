# app/core/security.py
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # 한국 시간 사용을 위한 zoneinfo 모듈
from jose import JWTError, jwt
from typing import Optional

# 시크릿 키와 알고리즘 설정 (실제 서비스에선 .env로 관리)
SECRET_KEY = "your-secret-key"  # TODO: .env로 분리 추천
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1시간 유효

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 액세스 토큰 생성 (한국 시간 기준)"""
    to_encode = data.copy()
    expire = datetime.now(ZoneInfo("Asia/Seoul")) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    """JWT 토큰 디코딩 (유효하지 않으면 None 반환)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
