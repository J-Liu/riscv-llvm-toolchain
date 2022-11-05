from pathlib import Path

from scripts.config import TARBALLS_ROOT, SRC_ROOT, BUILD_ROOT


def init_dir():
    Path(TARBALLS_ROOT).mkdir(parents=True, exist_ok=True)
    Path(SRC_ROOT).mkdir(parents=True, exist_ok=True)
    Path(BUILD_ROOT).mkdir(parents=True, exist_ok=True)
