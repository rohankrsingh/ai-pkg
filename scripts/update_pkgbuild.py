#!/usr/bin/env python3
import hashlib
import sys
from pathlib import Path
import re

def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def update_pkgbuild(pkgbuild_path: Path, wheel_path: Path):
    if not pkgbuild_path.exists():
        print(f"ERROR: {pkgbuild_path} does not exist")
        sys.exit(2)
    if not wheel_path.exists():
        print(f"ERROR: {wheel_path} does not exist")
        sys.exit(3)

    checksum = sha256sum(wheel_path)
    text = pkgbuild_path.read_text(encoding="utf-8")

    # Replace any existing sha256sums=(...) with the new checksum
    new_text, cnt = re.subn(
        r"sha256sums=\([^\)]*\)",
        f"sha256sums=('{checksum}')",
        text,
        flags=re.MULTILINE,
    )

    if cnt == 0:
        # If no sha256sums found, append it at the end
        new_text = text + f"\nsha256sums=('{checksum}')\n"

    pkgbuild_path.write_text(new_text, encoding="utf-8")
    print(f"✅ Updated {pkgbuild_path} with sha256sum={checksum}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: update_pkgbuild.py <PKGBUILD_PATH> <WHEEL_PATH>")
        sys.exit(1)
    update_pkgbuild(Path(sys.argv[1]), Path(sys.argv[2]))