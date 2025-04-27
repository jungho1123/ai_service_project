# app/scripts/init_db.py
import json, os, glob
from tqdm import tqdm
from app.core.config import get_settings
from app.core.database import get_db
from app.models.pill import Pill

settings = get_settings()
label_dir = settings.FALLBACK_LABEL_PATH

db = next(get_db())
try:
    for fp in tqdm(glob.glob(os.path.join(label_dir, "*_json/*.json"))):
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)
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
    db.commit()
    print("Pill 테이블 초기화 완료")
finally:
    db.close()
