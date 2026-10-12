from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# KITTI OXTS is logged at 10 Hz and the csv files carry no timestamps
DT = 0.1

# WGS84 ellipsoid
WGS84_A = 6378137.0
WGS84_E2 = 6.69437999014e-3

INT_COLUMNS = ["navstat", "numsats", "posmode", "velmode", "orimode"]


def build_features() -> Path:
    src_dir = DATA_DIR / "csv"
    out_dir = DATA_DIR / "cleaned"
    out_file = out_dir / "kitti.parquet"

    out_dir.mkdir(parents=True, exist_ok=True)

    frames = []
    for src_file in sorted(src_dir.glob("*.csv")):
        df = pd.read_csv(src_file)
        df.insert(0, "drive", src_file.stem)
        df.insert(1, "frame", np.arange(len(df)))
        frames.append(df)

    data = pd.concat(frames, ignore_index=True)

    numeric = data.select_dtypes("number")
    if not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("Found NaN or inf values in the input data")
    data[INT_COLUMNS] = data[INT_COLUMNS].astype(int)

    data = pd.concat(
        [add_features(group) for _, group in data.groupby("drive", sort=True)]
    )
    data = data.reset_index(drop=True)

    data.to_parquet(out_file, index=False)
    return out_file


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["speed"] = np.sqrt(df["vn"] ** 2 + df["ve"] ** 2 + df["vu"] ** 2)
    df["speed_2d"] = np.hypot(df["vn"], df["ve"])
    df["accel_mag"] = np.sqrt(df["ax"] ** 2 + df["ay"] ** 2 + df["az"] ** 2)
    df["gyro_mag"] = np.sqrt(df["wx"] ** 2 + df["wy"] ** 2 + df["wz"] ** 2)

    # Wrap the yaw difference to [-pi, pi]; the first frame of a drive has no previous one
    dyaw = df["yaw"].diff().fillna(0.0)
    df["heading_change"] = np.arctan2(np.sin(dyaw), np.cos(dyaw))
    df["yaw_rate_est"] = df["heading_change"] / DT

    df["east"], df["north"], df["up"] = geodetic_to_enu(
        df["lat"].to_numpy(),
        df["lon"].to_numpy(),
        df["alt"].to_numpy(),
        df["lat"].iloc[0],
        df["lon"].iloc[0],
        df["alt"].iloc[0],
    )
    return df


def geodetic_to_ecef(lat, lon, alt):
    lat, lon = np.radians(lat), np.radians(lon)
    n = WGS84_A / np.sqrt(1 - WGS84_E2 * np.sin(lat) ** 2)
    x = (n + alt) * np.cos(lat) * np.cos(lon)
    y = (n + alt) * np.cos(lat) * np.sin(lon)
    z = (n * (1 - WGS84_E2) + alt) * np.sin(lat)
    return x, y, z


def geodetic_to_enu(lat, lon, alt, lat0, lon0, alt0):
    x, y, z = geodetic_to_ecef(lat, lon, alt)
    x0, y0, z0 = geodetic_to_ecef(lat0, lon0, alt0)
    dx, dy, dz = x - x0, y - y0, z - z0

    lat0, lon0 = np.radians(lat0), np.radians(lon0)
    east = -np.sin(lon0) * dx + np.cos(lon0) * dy
    north = (
        -np.sin(lat0) * np.cos(lon0) * dx
        - np.sin(lat0) * np.sin(lon0) * dy
        + np.cos(lat0) * dz
    )
    up = (
        np.cos(lat0) * np.cos(lon0) * dx
        + np.cos(lat0) * np.sin(lon0) * dy
        + np.sin(lat0) * dz
    )
    return east, north, up


if __name__ == "__main__":
    destination = build_features()
    print("Path to cleaned parquet:", destination)
