from pathlib import Path

current_file_path = Path(__file__).absolute()
TOP_PATH = Path(current_file_path).parent.parent
BUILD_ROOT = TOP_PATH.joinpath('build')
PATCH_ROOT = TOP_PATH.joinpath('patches')
RESOURCES_ROOT = TOP_PATH.joinpath('resources')
SRC_ROOT = TOP_PATH.joinpath('src')
TARBALL_ROOT = TOP_PATH.joinpath('tarballs')

LINUX_VER = '6.0.7'
NEWLIB_VER = '4.2.0.20211231'
MUSL_VER = '1.2.3'
QEMU_VER = '7.1.0'

SUFFIX_XZ = 'tar.xz'
SUFFIX_BZ = 'tar.bz2'
SUFFIX_GZ = 'tar.gz'

LINUX_TARBALL = 'linux-' + LINUX_VER + '.' + SUFFIX_XZ
NEWLIB_TARBALL = 'newlib-' + NEWLIB_VER + '.' + SUFFIX_GZ
MUSL_TARBALL = 'musl-' + MUSL_VER + '.' + SUFFIX_GZ
QEMU_TARBALL = 'qemu-' + QEMU_VER + '.' + SUFFIX_XZ

LINUX_SITE = 'https://cdn.kernel.org/pub/linux/kernel/v6.x/'
LINUX_URL = LINUX_SITE + LINUX_TARBALL
MUSL_SITE = 'https://musl.libc.org/releases/'
MUSL_URL = MUSL_SITE + MUSL_TARBALL
NEWLIB_SITE = 'http://sourceware.org/pub/newlib/'
NEWLIB_URL = NEWLIB_SITE + NEWLIB_TARBALL
QEMU_SITE = 'https://download.qemu.org/'
QEMU_URL = QEMU_SITE + QEMU_TARBALL

LLVM_GIT_URL = 'https://github.com/llvm/llvm-project.git'
LLVM_PROJ_NAME = 'llvm-project'

PATCH_NEWLIB_C99 = PATCH_ROOT.joinpath('newlib-4.2.0.20211231-C99-build.diff')

NEWLIB_TRIPLE = 'riscv64-unknown-elf'
MUSL_TRIPLE = 'riscv64-unknown-linux-musl'
TOOLS_TO_BUILD = 'clang;lld'
TARGETS_TO_BUILD = 'RISCV'

LLVM_PROJ_ROOT = SRC_ROOT.joinpath(LLVM_PROJ_NAME)
SRC_LLVM = LLVM_PROJ_ROOT.joinpath('llvm')
SRC_COMPILER_RT = LLVM_PROJ_ROOT.joinpath('compiler-rt')
SRC_LIBUNWIND = LLVM_PROJ_ROOT.joinpath('libunwind')
SRC_LIBCXX = LLVM_PROJ_ROOT.joinpath('libcxx')
SRC_LIBCXXABI = LLVM_PROJ_ROOT.joinpath('libcxxabi')

SRC_LINUX = SRC_ROOT.joinpath('linux-' + LINUX_VER)
SRC_MUSL = SRC_ROOT.joinpath('musl-' + MUSL_VER)
SRC_NEWLIB = SRC_ROOT.joinpath('newlib-' + NEWLIB_VER)
SRC_QEMU = SRC_ROOT.joinpath('qemu-' + QEMU_VER)

BUILD_CLANG = BUILD_ROOT.joinpath('clang')
BUILD_MUSL = BUILD_ROOT.joinpath('musl')
BUILD_MUSL_HEADERS = BUILD_ROOT.joinpath('musl-headers')
BUILD_NEWLIB = BUILD_ROOT.joinpath('newlib')
BUILD_COMPILER_RT_MUSL = BUILD_ROOT.joinpath('compiler-rt-musl')
BUILD_COMPILER_RT_NEWLIB = BUILD_ROOT.joinpath('compiler-rt-elf')
BUILD_LIBUNWIND = BUILD_ROOT.joinpath('libunwind')
BUILD_LIBCXX = BUILD_ROOT.joinpath('libcxx')
BUILD_LIBCXXABI = BUILD_ROOT.joinpath('libcxxabi')
BUILD_QEMU = BUILD_ROOT.joinpath('qemu')

CLANG_TEMPLATE = RESOURCES_ROOT.joinpath('target-clang-template')
