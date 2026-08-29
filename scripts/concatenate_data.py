import argparse
from pathlib import Path
import re

DRIVE_PATTERN = re.compile(r"^\d{4}_\d{2}_\d{2}_drive_\d{4}_sync$")
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def build_output(monofile: bool) -> Path:
    src_dir = DATA_DIR / "raw"
    out_dir = DATA_DIR / "processed"

    # Create the data/processed/ directory if it doesn't exist yet
    # Do nothing if it already exists
    out_dir.mkdir(exist_ok=True)

    drives = sorted(
        x for x in src_dir.glob("*/*") if x.is_dir() and DRIVE_PATTERN.match(x.name)
    )

    for drive in drives:
        oxts_dir = drive / "oxts" / "data"
        if not oxts_dir.is_dir():
            continue
        outfile_name = f"{drive.name}.txt"
        concat_files(oxts_dir, out_dir / outfile_name)

    if monofile:
        concat_files(out_dir, out_dir / "combined.txt")
        for drive in drives:
            outfile_name = f"{drive.name}.txt"
            (out_dir / outfile_name).unlink(missing_ok=True)

    return out_dir


def concat_files(src_dir: Path, out_dir: Path) -> None:
    with open(out_dir, mode="w", encoding="utf-8") as outfile:
        for x in sorted(src_dir.iterdir()):
            if not x.is_file():
                continue
            if x.name == out_dir.name:
                continue
            if x.suffix != ".txt":
                continue
            with open(x, mode="r", encoding="utf-8") as infile:
                outfile.write(infile.read())

        return None


if __name__ == "__main__":
    # Add the option to have the output be one file, instead of
    # a separate output for each drive.
    parser = argparse.ArgumentParser(description="Concatenate oxts drive data")
    parser.add_argument("--monofile", action="store_true")
    args = parser.parse_args()

    destination = build_output(args.monofile)
    print("Path to processed files:", destination)
