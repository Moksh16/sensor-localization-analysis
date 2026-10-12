# sensor-localization-analysis

Exploratory analysis of the OXTS (GPS/IMU) data from the KITTI pose estimation dataset on Kaggle (`kubeedgeianvs/the-kitti-pose-estimation-dataset`).

## Setup

```
pip install -r requirements.txt
```

The download step needs Kaggle credentials for `kagglehub`.

## Running the pipeline

```
./run_eda.sh
```

This downloads the data if `data/raw` is missing, then runs the steps below. Each step can also be run alone with `make download`, `make concat`, `make csv` or `make features`. `make clean` removes the generated data.

| Script | Reads | Writes |
| --- | --- | --- |
| `scripts/download_data.py` | Kaggle | `data/raw/` |
| `scripts/concatenate_data.py` | `data/raw/` | `data/processed/<drive>.txt` (`--monofile` writes one `combined.txt`) |
| `scripts/build_csv.py` | `data/processed/` | `data/csv/<drive>.csv` |
| `scripts/feature_engineering.py` | `data/csv/` | `data/cleaned/kitti.parquet` |

`feature_engineering.py` adds `drive`, `frame`, speed and acceleration magnitudes, yaw change per frame, and east/north/up position relative to each drive's first GPS fix. It assumes the 10 Hz OXTS rate, since the CSVs have no timestamps.

`data/` is gitignored.
