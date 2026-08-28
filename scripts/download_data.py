from pathlib import Path
import shutil

import kagglehub

DATASET = "kubeedgeianvs/the-kitti-pose-estimation-dataset"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def download_dataset() -> Path:
    # Download the dataset via kagglehub
    cache_dir = Path(kagglehub.dataset_download(DATASET))

    # Creates both data/ and data/raw/ as needed
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Copies the dataset into DATA_DIR
    shutil.copytree(cache_dir / "data", DATA_DIR, dirs_exist_ok=True)

    return DATA_DIR


if __name__ == "__main__":
    destination = download_dataset()
    print("Path to dataset files:", destination)
