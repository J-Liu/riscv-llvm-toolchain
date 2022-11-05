from pathlib import Path

current_file_path = Path(__file__).absolute()
TOP_PATH = Path(current_file_path).parent.parent
BUILD_ROOT = TOP_PATH.joinpath('build')
SRC_ROOT = TOP_PATH.joinpath('src')
TARBALLS_ROOT = TOP_PATH.joinpath('tarballs')

LINUX_VER = '6.0.7'
NEWLIB_VER = '4.2.0.20211231'
MUSL_VER = '1.2.3'

SUFFIX_XZ = 'tar.xz'
SUFFIX_BZ = 'tar.bz2'
SUFFIX_GZ = 'tar.gz'

LINUX_TARBALL = 'linux-' + LINUX_VER + '.' + SUFFIX_XZ
NEWLIB_TARBALL = 'newlib-' + NEWLIB_VER + '.' + SUFFIX_GZ
MUSL_TARBALL = 'musl-' + MUSL_VER + '.' + SUFFIX_GZ
