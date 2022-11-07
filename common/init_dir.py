from pathlib import Path

from conf.conf import BUILD_ROOT, SRC_ROOT, TARBALL_ROOT


def init_dir():
    Path(TARBALL_ROOT).mkdir(parents=True, exist_ok=True)
    Path(SRC_ROOT).mkdir(parents=True, exist_ok=True)
    Path(BUILD_ROOT).mkdir(parents=True, exist_ok=True)
