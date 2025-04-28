# app/api/predict.py

from fastapi import APIRouter, UploadFile, File  # FastAPI의 APIRouter, 파일 업로드 관련 모듈 가져오기
from app.services import predict_service, pill_service  # 비즈니스 로직 서비스 모듈 가져오기
import json, pathlib  # JSON 파일 처리와 파일 경로 관리를 위한 모듈 가져오기

# APIRouter 인스턴스 생성, URL 경로 접두사는 '/predict', Swagger UI 상단 카테고리 이름은 'Predict'
router = APIRouter(prefix="/predict", tags=["Predict"])

# 프로젝트 루트 디렉터리를 기준으로 data 폴더의 classid_to_itemseq.json 파일 경로를 설정
BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

# class_id를 item_seq로 매핑하는 JSON 파일을 메모리에 로딩
CID2SEQ = json.loads((BASE_DIR / "data" / "classid_to_itemseq.json").read_text(encoding="utf-8"))

@router.post("")
async def predict(file: UploadFile = File(...)):  # POST 메소드로 파일 업로드를 받는 API 엔드포인트 정의
    img_bytes = await file.read()  # 업로드된 파일을 비동기적으로 읽어 바이트 데이터로 변환
    
    # predict_service를 통해 이미지 데이터를 모델에 입력하여 class_id 예측 및 신뢰도(confidence) 계산
    class_id, conf = predict_service.predict(img_bytes, threshold=0.7)

    if not class_id:
        # 모델이 자신 있게 예측하지 못한 경우, 사용자에게 검색을 추천하는 메시지 반환
        return {
            "message": "모델이 정확히 인식하지 못했습니다.",
            "confidence": conf,
            "search_suggest": True
        }

    # 예측된 class_id를 기반으로 약 정보(fallback 포함)를 조회
    info = pill_service.resolve_pill_info(class_id, CID2SEQ)

    # 결과에 예측된 class_id와 신뢰도를 추가하여 최종 응답 구성
    info.update({"class_id": class_id, "confidence": conf})
    return info  # 완성된 약 정보 반환
