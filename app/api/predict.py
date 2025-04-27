# app/api/predict.py
from fastapi import APIRouter, UploadFile, File
from app.services import predict_service, pill_service
import json, pathlib

router = APIRouter(prefix="/predict", tags=["Predict"])
BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
CID2SEQ = json.loads((BASE_DIR/"data"/"classid_to_itemseq.json").read_text(encoding="utf-8"))

@router.post("")
async def predict(file: UploadFile = File(...)):
    img_bytes = await file.read()
    class_id, conf = predict_service.predict(img_bytes, threshold=0.5)
    if not class_id:
        return {"message": "모델이 정확히 인식하지 못했습니다.", "confidence": conf, "search_suggest": True}
    info = pill_service.resolve_pill_info(class_id, CID2SEQ)
    info.update({"class_id": class_id, "confidence": conf})
    return info
