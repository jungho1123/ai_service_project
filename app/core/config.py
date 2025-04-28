from functools import lru_cache  # 결과를 캐시하여 성능을 최적화하는 데코레이터 가져오기
from pydantic import BaseSettings, AnyHttpUrl  # 환경 설정 및 URL 타입 검증을 위한 모듈 가져오기

class Settings(BaseSettings):  # Pydantic의 BaseSettings를 상속하여 환경변수 기반 설정 클래스 정의
    DATABASE_URL: str  # 데이터베이스 연결 문자열 (필수)
    API_SERVICE_KEY: str  # 공공데이터 API 서비스 키 (필수)
    FALLBACK_LABEL_PATH: str = ""  # fallback용 JSON 파일 경로 (기본값 빈 문자열)
    ALLOWED_ORIGINS: list[AnyHttpUrl] | list[str] = ["*"]  # CORS 허용 Origin 목록, 기본값은 모두 허용

    class Config:  # 내부 설정 클래스로 .env 파일을 환경변수 소스로 지정
        env_file = ".env"  # 환경변수를 읽어올 파일명 지정

@lru_cache  # get_settings 함수를 호출할 때마다 결과를 메모리에 저장하여 재사용하도록 설정
def get_settings() -> Settings:
    return Settings()  # Settings 인스턴스를 생성하여 반환
