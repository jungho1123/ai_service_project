# app/core/mappings.py
from pathlib import Path
import json
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parents[2]

@lru_cache
def get_classid_to_itemseq() -> dict[str, int]:
    """
    class_id → itemSeq 매핑을 1회만 읽어 캐시합니다.
    """
    path = BASE_DIR / "data" / "classid_to_itemseq.json"
    return json.loads(path.read_text(encoding="utf-8"))
