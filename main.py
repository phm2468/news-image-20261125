#!/usr/bin/env python3
"""Writes the entry image to /output/entry.png.

The image (entry.png, built by compose.py from the day's reporting:
Hormuz as the lead, Riyadh, Gaza and Odesa below the fold, COP31 and
the Huawei verdict in the ticker) is copied byte for byte, so every
run produces exactly the same file: no input, no network, fully
deterministic.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
