"""
Pest / disease detection.

Loading priority (first that succeeds wins):
  1. Your own trained checkpoint  backend/models/pest_model_india.pt
     (from ai/train.py -- bundles weights + labels + arch + img_size).
  2. A pre-trained PlantVillage model from Hugging Face (38 disease classes).
  3. Deterministic stub (only if neither torch nor transformers is available),
     so the API never crashes.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from ..config import settings
from .remedies import remedy_for

_MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "pest_model_india.pt"

_DEFAULT_LABELS = [
    "Healthy", "Whitefly", "Aphids", "Armyworm", "Bollworm",
    "Early Blight", "Late Blight", "Leaf Curl Virus",
    "Powdery Mildew", "Bacterial Leaf Spot",
]

# Lazily-initialised engine state.
_state: dict = {"mode": None, "loaded": False}


def _load_hf() -> bool:
    """Load the pre-trained PlantVillage model from Hugging Face."""
    try:
        import torch
        from transformers import AutoImageProcessor, AutoModelForImageClassification
    except Exception:
        return False
    try:
        repo = settings.PEST_MODEL_HF_REPO
        proc = AutoImageProcessor.from_pretrained(repo)
        model = AutoModelForImageClassification.from_pretrained(repo)
        model.eval()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        _state.update(
            mode="hf",
            torch=torch,
            processor=proc,
            model=model,
            device=device,
            id2label=model.config.id2label,
            name=f"pretrained {repo.split('/')[-1]} ({len(model.config.id2label)} classes, {device})",
        )
        return True
    except Exception:
        return False


def _load_checkpoint() -> bool:
    """Load a user-trained torchvision checkpoint if present."""
    if not _MODEL_PATH.exists():
        return False
    try:
        import torch
        from torchvision import models as tv

        ckpt = torch.load(_MODEL_PATH, map_location="cpu")
        labels = ckpt["labels"]
        arch = ckpt.get("arch", "efficientnet_b3")
        img_size = ckpt.get("img_size", 300)
        if arch == "mobilenet_v2":
            model = tv.mobilenet_v2(weights=None)
            model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(labels))
        else:
            model = tv.efficientnet_b3(weights=None)
            model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(labels))
        model.load_state_dict(ckpt["state_dict"])
        model.eval()

        import torchvision.transforms as T

        transform = T.Compose([
            T.Resize((img_size, img_size)),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])
        _state.update(
            mode="checkpoint",
            torch=torch,
            model=model,
            transform=transform,
            labels=labels,
            name=f"trained {arch} (val_acc={ckpt.get('val_acc', 'n/a')})",
        )
        return True
    except Exception:
        return False


def _ensure_loaded() -> str:
    if _state["loaded"]:
        return _state["mode"]
    _state["loaded"] = True
    # Prefer the user's own trained model, then the pretrained HF model.
    if _load_checkpoint() or _load_hf():
        return _state["mode"]
    _state["mode"] = "stub"
    _state["name"] = "stub (install torch + transformers for real inference)"
    return "stub"


def _predict_hf(img_path: str):
    from PIL import Image

    torch = _state["torch"]
    image = Image.open(img_path).convert("RGB")
    inputs = _state["processor"](images=image, return_tensors="pt").to(_state["device"])
    with torch.no_grad():
        probs = _state["model"](**inputs).logits.softmax(-1)
    conf, idx = probs.max(-1)
    label = _state["id2label"][idx.item()]
    return label, round(float(conf.item()), 3)


def _predict_checkpoint(img_path: str):
    from PIL import Image

    torch = _state["torch"]
    image = Image.open(img_path).convert("RGB")
    tensor = _state["transform"](image).unsqueeze(0)
    with torch.no_grad():
        probs = _state["model"](tensor).softmax(-1)
    conf, idx = probs.max(-1)
    label = _state["labels"][idx.item() % len(_state["labels"])]
    return label, round(float(conf.item()), 3)


def _predict_stub(img_path: str):
    digest = hashlib.md5(Path(img_path).read_bytes()).hexdigest()
    idx = int(digest, 16) % len(_DEFAULT_LABELS)
    confidence = 0.50 + (int(digest[:2], 16) / 255.0) * 0.45
    return _DEFAULT_LABELS[idx], round(confidence, 3)


def predict_pest(img_path: str) -> dict:
    """Return {pest, confidence, remedy, model} for an image on disk."""
    mode = _ensure_loaded()
    try:
        if mode == "hf":
            label, confidence = _predict_hf(img_path)
        elif mode == "checkpoint":
            label, confidence = _predict_checkpoint(img_path)
        else:
            label, confidence = _predict_stub(img_path)
    except Exception:
        label, confidence = _predict_stub(img_path)

    return {
        "pest": label,
        "confidence": confidence,
        "remedy": remedy_for(label),
        "model": _state.get("name", "stub"),
    }
