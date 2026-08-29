from pathlib import Path
import shutil

import kagglehub

DATASET = "kubeedgeianvs/the-kitti-pose-estimation-dataset"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def download_dataset() -> Path:
    # Download the dataset via kagglehub
    cache_dir = Path(kagglehub.dataset_download(DATASET))
    raw_dir = DATA_DIR / "raw"

    # Creates both data/ and data/raw/ as needed
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Copies the dataset into raw_dir
    shutil.copytree(cache_dir / "data", raw_dir, dirs_exist_ok=True)

    return raw_dir


if __name__ == "__main__":
    destination = download_dataset()
    print("Path to dataset files:", destination)
