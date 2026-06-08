# Kisan Sathi — Pest Detection Model Training

Train an EfficientNet-B3 classifier on crop pest/disease images and drop the
result into the backend. The backend auto-loads it on next start.

## Why not train on your laptop?
Training needs the multi-GB image datasets **and** a GPU (CPU training takes
many hours). The easiest free option is **Google Colab** (T4 GPU).

## Datasets (free)
- **PlantVillage** — ~54k leaf images, 38 disease classes (Kaggle).
- **Pestopia** — Indian pests & pesticides (Kaggle).
- **Bollworm** — cotton bollworm image set (Kaggle).

Download, then arrange them in ImageFolder format:

```
data/
  train/<ClassName>/*.jpg
  val/<ClassName>/*.jpg
```

Tip: keep ~80% of each class in `train/` and ~20% in `val/`.

## Train on Google Colab (recommended)
1. Open https://colab.research.google.com → New notebook.
2. Runtime → Change runtime type → **T4 GPU**.
3. In a cell:
   ```python
   !pip install torch torchvision tqdm
   # upload train.py and your data/ folder (or mount Google Drive)
   !python train.py --data ./data --epochs-head 3 --epochs-finetune 6
   ```
4. Download the produced `pest_model_india.pt`.

## Train locally (if you have an NVIDIA GPU)
```bat
cd "e:\kisan sathi\ai"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python train.py --data .\data --epochs-head 3 --epochs-finetune 5
```

## Plug it into the backend
Place the trained file here:

```
backend/models/pest_model_india.pt
```

Restart the backend. `GET /pest/report` will now report
`"model": "trained efficientnet_b3 (val_acc=...)"` and use your real classes.
No code changes needed — the checkpoint carries its own labels.
