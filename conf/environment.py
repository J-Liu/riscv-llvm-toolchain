import os

from common.user_input import get_build_type, get_prefix
from conf.conf import BUILD_CLANG, BUILD_COMPILER_RT_MUSL, \
    BUILD_COMPILER_RT_NEWLIB, BUILD_MUSL, BUILD_MUSL_HEADERS, BUILD_NEWLIB, \
    BUILD_QEMU, BUILD_ROOT, BUILD_RUNTIMES_ELF, BUILD_RUNTIMES_MUSL, \
    MUSL_TRIPLE, NEWLIB_TRIPLE, RUNTIMES_TO_BUILD, SRC_COMPILER_RT, SRC_LINUX, \
    SRC_LLVM, SRC_MUSL, SRC_NEWLIB, SRC_QEMU, SRC_ROOT, SRC_RUNTIMES, \
    TARBALL_ROOT, TARGETS_TO_BUILD, TOOLS_TO_BUILD


def init_env():
    os.environ['JOBS'] = '-j32'

    prefix = get_prefix()
    os.environ['CLANG_PREFIX'] = prefix
    old_path = os.environ.get('PATH')
    os.environ['PATH'] = prefix + '/bin:' + old_path

    os.environ['MUSL_TRIPLE'] = MUSL_TRIPLE
    os.environ['NEWLIB_TRIPLE'] = NEWLIB_TRIPLE

    os.environ['MUSL_SYSROOT'] = os.environ.get('CLANG_PREFIX') + '/sysroot'
    os.environ['NEWLIB_SYSROOT'] = os.environ.get(
        'CLANG_PREFIX') + '/' + NEWLIB_TRIPLE

    os.environ['MUSL_CFLAGS'] = \
        '--target=${MUSL_TRIPLE} --sysroot=${MUSL_SYSROOT}'
    os.environ['NEWLIB_CFLAGS'] = \
        '--target=${NEWLIB_TRIPLE} --sysroot=${NEWLIB_SYSROOT}'
    os.environ['MUSL_CXXFLAGS'] = os.environ.get('MUSL_CFLAGS')
    os.environ['NEWLIB_CXXFLAGS'] = os.environ.get('NEWLIB_CFLAGS')
    os.environ['CLANG_LDFLAGS'] = '-fuse-ld=lld'
    os.environ['MUSL_RUNTIMES_CFLAGS'] = '--target=${MUSL_TRIPLE}'
    os.environ['NEWLIB_RUNTIMES_CFLAGS'] = '--target=${NEWLIB_TRIPLE}'
    os.environ['MUSL_RUNTIMES_CXXFLAGS'] = os.environ.get(
        'MUSL_RUNTIMES_CFLAGS')
    os.environ['NEWLIB_RUNTIMES_CXXFLAGS'] = os.environ.get(
        'NEWLIB_RUNTIMES_CFLAGS')

    os.environ['TOOLS_TO_BUILD'] = TOOLS_TO_BUILD
    os.environ['TARGETS_TO_BUILD'] = TARGETS_TO_BUILD
    os.environ['RUNTIMES_TO_BUILD'] = RUNTIMES_TO_BUILD
    os.environ['BUILE_TYPE'] = get_build_type()

    os.environ['TARBALL_ROOT'] = TARBALL_ROOT.as_posix()
    os.environ['SRC_ROOT'] = SRC_ROOT.as_posix()
    os.environ['BUILD_ROOT'] = BUILD_ROOT.as_posix()

    os.environ['SRC_LINUX'] = SRC_LINUX.as_posix()
    os.environ['SRC_MUSL'] = SRC_MUSL.as_posix()
    os.environ['SRC_NEWLIB'] = SRC_NEWLIB.as_posix()
    os.environ['SRC_LLVM'] = SRC_LLVM.as_posix()
    os.environ['SRC_COMPILER_RT'] = SRC_COMPILER_RT.as_posix()
    os.environ['SRC_RUNTIMES'] = SRC_RUNTIMES.as_posix()
    os.environ['SRC_QEMU'] = SRC_QEMU.as_posix()

    os.environ['BUILD_MUSL'] = BUILD_MUSL.as_posix()
    os.environ['BUILD_MUSL_HEADERS'] = BUILD_MUSL_HEADERS.as_posix()
    os.environ['BUILD_NEWLIB'] = BUILD_NEWLIB.as_posix()
    os.environ['BUILD_CLANG'] = BUILD_CLANG.as_posix()
    os.environ['BUILD_COMPILER_RT_NEWLIB'] = BUILD_COMPILER_RT_NEWLIB.as_posix()
    os.environ['BUILD_COMPILER_RT_MUSL'] = BUILD_COMPILER_RT_MUSL.as_posix()
    os.environ['BUILD_RUNTIMES_NEWLIB'] = BUILD_RUNTIMES_ELF.as_posix()
    os.environ['BUILD_RUNTIMES_MUSL'] = BUILD_RUNTIMES_MUSL.as_posix()
    os.environ['BUILD_QEMU'] = BUILD_QEMU.as_posix()
