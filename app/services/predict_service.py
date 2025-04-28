# app/services/predict_service.py

from pathlib import Path  # 파일 경로를 다루기 위한 pathlib 모듈 임포트
import torch, io, json  # PyTorch, 바이트 IO 처리, JSON 모듈 임포트
from torchvision import transforms  # 이미지 전처리용 torchvision transforms 모듈 임포트
from torchvision.models import efficientnet_b3  # EfficientNet-b3 모델 구조 임포트
from PIL import Image, UnidentifiedImageError  # 이미지 처리 및 에러 핸들링을 위한 Pillow 모듈 임포트

BASE_DIR = Path(__file__).resolve().parents[2]  # 프로젝트 루트 디렉토리 경로 계산
MODEL_PATH = BASE_DIR / "model" / "best_model.pth"  # 학습된 모델 파일 경로 설정
CLASS_MAP_PATH = BASE_DIR / "data" / "class_idx_to_id.json"  # 클래스 인덱스 ↔ class_id 매핑 파일 경로 설정

IDX2CID: dict[str, str] = json.loads(CLASS_MAP_PATH.read_text(encoding="utf-8"))  # 매핑 파일을 읽어 딕셔너리로 변환

# 이미지 전처리 파이프라인 정의: Resize → CenterCrop → Tensor 변환 → 정규화
_preproc = transforms.Compose([
    transforms.Resize(300),
    transforms.CenterCrop(300),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

_model: torch.nn.Module | None = None  # 학습된 모델 객체 (초기에는 None)
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # GPU 사용 가능 여부에 따라 디바이스 설정

def _load_model() -> torch.nn.Module:  # 학습된 모델을 메모리에 로드하는 함수
    global _model
    if _model is None:
        m = efficientnet_b3(weights=None)  # Pretrained 가중치 없이 EfficientNet-b3 모델 구조 생성
        m.classifier[1] = torch.nn.Linear(m.classifier[1].in_features, len(IDX2CID))  # 분류기 레이어 출력 크기 수정
        m.load_state_dict(torch.load(MODEL_PATH, map_location=_device))  # 학습된 가중치 로드
        m.eval().to(_device)  # 평가 모드 전환 및 디바이스 이동
        _model = m
    return _model

def predict(image_bytes: bytes, threshold: float = 0.5) -> tuple[str | None, float]:  # 이미지를 입력받아 class_id를 예측하는 함수
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # 업로드된 이미지를 RGB 포맷으로 변환
    except (UnidentifiedImageError, OSError):
        return None, 0.0  # 잘못된 이미지 파일이면 None 반환

    tensor = _preproc(img).unsqueeze(0).to(_device)  # 전처리 후 배치 차원을 추가하고 디바이스로 이동
    with torch.no_grad():  # 추론 시에는 그래디언트 계산 비활성화
        probs = torch.nn.functional.softmax(_load_model()(tensor), dim=1)  # 모델 예측 후 softmax 적용
        conf, idx = torch.max(probs, dim=1)  # 가장 높은 확률과 인덱스 추출
        cid = IDX2CID.get(str(idx.item()))  # 예측 인덱스를 class_id로 변환
        return (cid if conf.item() >= threshold else None, conf.item())  # threshold 기준으로 결과 반환
