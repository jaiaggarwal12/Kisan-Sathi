"""
Kisan Sathi - Pest / disease detection model training.

Transfer-learning on EfficientNet-B3 (ImageNet pretrained) using a folder of
labelled images (PlantVillage / Pestopia / Bollworm, merged). Two-stage:
  Stage 1: freeze the backbone, train only the new classifier head.
  Stage 2: unfreeze everything and fine-tune with a small learning rate.

The best checkpoint is saved as a single .pt file that bundles the weights,
the class labels, the architecture name and the input image size, so the
backend can load it without guessing anything.

------------------------------------------------------------------
DATASET LAYOUT (ImageFolder format)
------------------------------------------------------------------
  data/
    train/
      Healthy/            img1.jpg img2.jpg ...
      Early_Blight/       ...
      Whitefly/           ...
    val/
      Healthy/            ...
      Early_Blight/       ...
      Whitefly/           ...

Each sub-folder name becomes a class label.

------------------------------------------------------------------
RUN
------------------------------------------------------------------
  pip install -r requirements.txt
  python train.py --data ./data --epochs-head 3 --epochs-finetune 5

Output: ../backend/models/pest_model_india.pt
Use a GPU (Google Colab "T4 GPU" runtime is free and works well).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from tqdm import tqdm

ARCH = "efficientnet_b3"
IMG_SIZE = 300  # EfficientNet-B3 native input size


def build_loaders(data_dir: Path, batch_size: int):
    train_tf = transforms.Compose(
        [
            transforms.RandomResizedCrop(IMG_SIZE, scale=(0.7, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(20),
            transforms.ColorJitter(0.2, 0.2, 0.2, 0.05),
            transforms.GaussianBlur(3),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    val_tf = transforms.Compose(
        [
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    # Two supported layouts:
    #  (a) data/train/<class>/* and data/val/<class>/*   -> use as-is
    #  (b) data/<class>/*                                -> auto 80/20 split
    if (data_dir / "train").exists() and (data_dir / "val").exists():
        train_ds = datasets.ImageFolder(data_dir / "train", transform=train_tf)
        val_ds = datasets.ImageFolder(data_dir / "val", transform=val_tf)
        classes = train_ds.classes
    else:
        import torch

        full = datasets.ImageFolder(data_dir, transform=train_tf)
        classes = full.classes
        val_size = max(1, int(0.2 * len(full)))
        train_size = len(full) - val_size
        gen = torch.Generator().manual_seed(42)
        train_ds, val_subset = torch.utils.data.random_split(
            full, [train_size, val_size], generator=gen
        )
        # Use validation transforms (no augmentation) for the val subset.
        val_base = datasets.ImageFolder(data_dir, transform=val_tf)
        val_ds = torch.utils.data.Subset(val_base, val_subset.indices)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=2)
    return train_loader, val_loader, classes


def build_model(num_classes: int, arch: str = ARCH):
    if arch == "mobilenet_v2":
        model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    else:
        model = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.IMAGENET1K_V1)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    return model


def set_backbone_trainable(model, trainable: bool):
    for name, param in model.named_parameters():
        if "classifier" not in name:
            param.requires_grad = trainable


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    correct = total = 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        preds = model(x).argmax(1)
        correct += (preds == y).sum().item()
        total += y.size(0)
    return correct / max(total, 1)


def run_epoch(model, loader, optimizer, criterion, device, desc):
    model.train()
    running = 0.0
    for x, y in tqdm(loader, desc=desc):
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()
        running += loss.item()
    return running / max(len(loader), 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("./data"))
    parser.add_argument("--out", type=Path, default=Path("../backend/models/pest_model_india.pt"))
    parser.add_argument("--epochs-head", type=int, default=3)
    parser.add_argument("--epochs-finetune", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--arch", choices=["efficientnet_b3", "mobilenet_v2"], default=ARCH)
    args = parser.parse_args()

    global IMG_SIZE
    IMG_SIZE = 224 if args.arch == "mobilenet_v2" else 300

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device} | arch: {args.arch} | img_size: {IMG_SIZE}")

    train_loader, val_loader, classes = build_loaders(args.data, args.batch_size)
    print(f"Classes ({len(classes)}): {classes}")

    model = build_model(len(classes), args.arch).to(device)
    criterion = nn.CrossEntropyLoss()
    best_acc = 0.0
    args.out.parent.mkdir(parents=True, exist_ok=True)

    def maybe_save(acc):
        nonlocal best_acc
        if acc > best_acc:
            best_acc = acc
            torch.save(
                {
                    "state_dict": model.state_dict(),
                    "labels": classes,
                    "arch": args.arch,
                    "img_size": IMG_SIZE,
                    "val_acc": acc,
                },
                args.out,
            )
            print(f"  saved new best -> {args.out} (val acc {acc:.3f})")

    # Stage 1: train head only.
    set_backbone_trainable(model, False)
    opt = torch.optim.Adam(model.classifier.parameters(), lr=1e-3)
    for e in range(args.epochs_head):
        loss = run_epoch(model, train_loader, opt, criterion, device, f"head {e+1}")
        acc = evaluate(model, val_loader, device)
        print(f"[head {e+1}] loss={loss:.3f} val_acc={acc:.3f}")
        maybe_save(acc)

    # Stage 2: fine-tune the whole network.
    set_backbone_trainable(model, True)
    opt = torch.optim.Adam(model.parameters(), lr=1e-4)
    for e in range(args.epochs_finetune):
        loss = run_epoch(model, train_loader, opt, criterion, device, f"finetune {e+1}")
        acc = evaluate(model, val_loader, device)
        print(f"[finetune {e+1}] loss={loss:.3f} val_acc={acc:.3f}")
        maybe_save(acc)

    print(f"Done. Best val accuracy: {best_acc:.3f}")
    # Also write labels next to the model for quick reference.
    (args.out.parent / "labels.json").write_text(json.dumps(classes, indent=2))


if __name__ == "__main__":
    main()
