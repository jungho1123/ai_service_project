# app/services/auth_service.py
from passlib.context import CryptContext

# 비밀번호 암호화를 위한 Bcrypt 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """비밀번호를 bcrypt 해시로 암호화"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """입력된 비밀번호와 저장된 해시가 일치하는지 확인"""
    return pwd_context.verify(plain_password, hashed_password)
