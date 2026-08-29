import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

OXTS_HEADERS = [
    "lat",
    "lon",
    "alt",
    "roll",
    "pitch",
    "yaw",
    "vn",
    "ve",
    "vf",
    "vl",
    "vu",
    "ax",
    "ay",
    "az",
    "af",
    "al",
    "au",
    "wx",
    "wy",
    "wz",
    "wf",
    "wl",
    "wu",
    "pos_accuracy",
    "vel_accuracy",
    "navstat",
    "numsats",
    "posmode",
    "velmode",
    "orimode",
]


def build_csv() -> Path:
    src_dir = DATA_DIR / "processed"
    out_dir = DATA_DIR / "csv"
    
    out_dir.mkdir(exist_ok=True)

    for src_file in sorted(src_dir.glob("*.txt")):
        stem = src_file.stem
        headerless_file = out_dir / f"{stem}.headerless.csv"
        final_file = out_dir / f"{stem}.csv"

        space_to_csv(src_file, headerless_file)
        add_headers(OXTS_HEADERS, headerless_file, final_file)
        headerless_file.unlink()

    return out_dir


def space_to_csv(src_file: Path, out_file: Path) -> None:
    with open(out_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        with open(src_file, mode="r", encoding="utf-8") as infile:
            for line in infile:
                writer.writerow(line.split())


def add_headers(headers: list[str], src_file: Path, out_file: Path) -> None:
    with open(out_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        with open(src_file, mode="r", encoding="utf-8", newline="") as infile:
            for row in csv.reader(infile):
                writer.writerow(row)


if __name__ == "__main__":
    destination = build_csv()
    print("Path to CSV files:", destination)
