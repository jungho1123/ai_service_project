# app/services/predict_service.py
from pathlib import Path
import torch, io, json
from torchvision import transforms
from torchvision.models import efficientnet_b3
from PIL import Image, UnidentifiedImageError

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "model" / "best_model.pth"
CLASS_MAP_PATH = BASE_DIR / "data" / "class_idx_to_id.json"

IDX2CID: dict[str, str] = json.loads(CLASS_MAP_PATH.read_text(encoding="utf-8"))

_preproc = transforms.Compose([
    transforms.Resize(300), transforms.CenterCrop(300),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

_model: torch.nn.Module | None = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def _load_model() -> torch.nn.Module:
    global _model
    if _model is None:
        m = efficientnet_b3(weights=None)
        m.classifier[1] = torch.nn.Linear(m.classifier[1].in_features,
                                          len(IDX2CID))
        m.load_state_dict(torch.load(MODEL_PATH, map_location=_device))
        m.eval().to(_device)
        _model = m
    return _model

def predict(image_bytes: bytes, threshold: float = 0.5) -> tuple[str | None, float]:
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError):
        # 잘못된 형식의 파일 업로드
        return None, 0.0

    tensor = _preproc(img).unsqueeze(0).to(_device)
    with torch.no_grad():
        probs = torch.nn.functional.softmax(_load_model()(tensor), dim=1)
        conf, idx = torch.max(probs, dim=1)
        cid = IDX2CID.get(str(idx.item()))
        return (cid if conf.item() >= threshold else None, conf.item())
