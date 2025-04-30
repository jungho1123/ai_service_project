# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.database import get_db
from app.models.user import User
from app.services.auth_service import hash_password, verify_password
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# 요청/응답 스키마
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        name=payload.name,
    )
    db.add(user)
    db.commit()
    return {"message": "회원가입 완료"}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
