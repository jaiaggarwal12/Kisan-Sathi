"""
Download a crop pest/disease dataset from Kaggle into ./data (ImageFolder).

Setup (one time):
  1. Create a free Kaggle account: https://www.kaggle.com
  2. Account -> Settings -> "Create New Token" -> downloads kaggle.json
  3. Put kaggle.json at  C:\\Users\\<you>\\.kaggle\\kaggle.json
     (or set KAGGLE_USERNAME and KAGGLE_KEY environment variables)

Run:
  python download_data.py                 # default: PlantVillage
  python download_data.py --dataset emmarex/plantdisease

The script copies the dataset into ./data/<class>/* so train.py can auto-split.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

# A few well-known crop datasets on Kaggle (slug -> note).
PRESETS = {
    "plantvillage": "emmarex/plantdisease",          # ~20k leaf images, 15 classes
    "plantvillage-full": "abdallahalidev/plantvillage-dataset",  # ~54k, 38 classes
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="plantvillage",
                        help="Kaggle slug or a preset name: " + ", ".join(PRESETS))
    parser.add_argument("--out", type=Path, default=Path("./data"))
    args = parser.parse_args()

    slug = PRESETS.get(args.dataset, args.dataset)
    print(f"Downloading '{slug}' from Kaggle ...")

    import kagglehub

    path = Path(kagglehub.dataset_download(slug))
    print(f"Downloaded to cache: {path}")

    # Find the deepest folder that contains class sub-folders of images.
    def looks_like_imagefolder(p: Path) -> bool:
        subdirs = [d for d in p.iterdir() if d.is_dir()]
        if not subdirs:
            return False
        return any(any(f.suffix.lower() in {".jpg", ".jpeg", ".png"} for f in d.iterdir() if f.is_file())
                   for d in subdirs)

    source = path
    candidates = [path] + [d for d in path.rglob("*") if d.is_dir()]
    for c in candidates:
        if looks_like_imagefolder(c):
            source = c
            break

    print(f"Using image root: {source}")
    args.out.mkdir(parents=True, exist_ok=True)
    for cls_dir in source.iterdir():
        if cls_dir.is_dir():
            dest = args.out / cls_dir.name
            if not dest.exists():
                print(f"  linking {cls_dir.name} ...")
                shutil.copytree(cls_dir, dest)
    print(f"Done. Dataset ready at {args.out.resolve()}")
    print("Now run:  python train.py --data ./data --arch efficientnet_b3")


if __name__ == "__main__":
    main()
