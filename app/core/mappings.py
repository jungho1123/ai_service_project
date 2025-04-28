# app/core/mappings.py

from pathlib import Path  # 파일 및 디렉터리 경로를 다루기 위한 pathlib 모듈 임포트
import json  # JSON 파일 읽기/쓰기를 위한 모듈 임포트
from functools import lru_cache  # 함수 결과를 메모리에 캐싱하는 데코레이터 임포트

BASE_DIR = Path(__file__).resolve().parents[2]  # 현재 파일을 기준으로 프로젝트 루트 디렉터리 경로 계산

@lru_cache  # 함수 결과를 캐시하여 매번 파일을 읽지 않고 성능을 최적화
def get_classid_to_itemseq() -> dict[str, int]:  # class_id를 item_seq로 매핑하는 딕셔너리 반환
    """
    class_id → itemSeq 매핑을 1회만 읽어 캐시합니다.
    """
    path = BASE_DIR / "data" / "classid_to_itemseq.json"  # 매핑 정보가 저장된 JSON 파일 경로 설정
    return json.loads(path.read_text(encoding="utf-8"))  # 파일을 읽고 JSON 객체로 파싱하여 반환
