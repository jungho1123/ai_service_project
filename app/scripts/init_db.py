# app/scripts/init_db.py

import json, os, glob  # JSON 처리, 파일 경로 조작, 파일 검색을 위한 표준 라이브러리 임포트
from tqdm import tqdm  # 진행 상황 표시를 위한 tqdm 라이브러리 임포트
from app.core.config import get_settings  # 환경 설정 불러오기
from app.core.database import get_db  # 데이터베이스 세션 생성 함수 불러오기
from app.models.pill import Pill  # Pill ORM 모델 임포트

settings = get_settings()  # 환경 설정 인스턴스 생성
label_dir = settings.FALLBACK_LABEL_PATH  # fallback JSON 파일들이 위치한 디렉터리 경로 설정

db = next(get_db())  # 데이터베이스 세션 객체 생성
try:
    # 지정한 디렉터리 내부의 *_json/*.json 파일들을 순회
    for fp in tqdm(glob.glob(os.path.join(label_dir, "*_json/*.json"))):
        with open(fp, encoding="utf-8") as f:  # JSON 파일을 열고
            data = json.load(f)  # JSON 데이터를 파싱

        # JSON 데이터 기반으로 Pill 객체를 생성하거나 갱신
        db.merge(Pill(
            class_id=data["class_id"],
            dl_name=data.get("dl_name"),
            dl_material=data.get("dl_material"),
            dl_company=data.get("dl_company"),
            di_company_mf=data.get("di_company_mf"),
            di_class_no=data.get("di_class_no"),
            di_etc_otc_code=data.get("di_etc_otc_code"),
            di_edi_code=data.get("di_edi_code"),
            item_seq=data.get("item_seq"),
            img_key=data.get("img_key"),
        ))
    db.commit()  # 모든 변경사항을 커밋하여 데이터베이스에 반영
    print("Pill 테이블 초기화 완료")  # 완료 메시지 출력
finally:
    db.close()  # 세션을 안전하게 닫아 리소스 해제
