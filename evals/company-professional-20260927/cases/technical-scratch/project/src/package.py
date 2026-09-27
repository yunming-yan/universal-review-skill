"""Deliberately unsafe package builder for the review fixture."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="release/review-package.zip")
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = root / arguments.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in root.rglob("*"):
            if path.is_file() and path != output:
                archive.write(path, path.relative_to(root))
    print(output)


if __name__ == "__main__":
    main()
