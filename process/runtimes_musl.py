from common.user_input import get_libc_type
from conf.conf import BUILD_RUNTIMES_MUSL
from utils.record_step import is_runtimes_musl_built, \
    is_runtimes_musl_configured, is_runtimes_musl_installed, \
    runtimes_musl_built, runtimes_musl_configured, runtimes_musl_installed
from utils.run_shell import run_shell

config_args = \
    '''
    -G Ninja \
    -DCMAKE_AR=${CLANG_PREFIX}/bin/llvm-ar \
    -DCMAKE_ASM_FLAGS=${MUSL_RUNTIMES_FLAGS} \
    -DCMAKE_BUILD_TYPE=MinSizeRel \
    -DCMAKE_CXX_COMPILER=${CLANG_PREFIX}/bin/clang++ \
    -DCMAKE_CXX_COMPILER_TARGET=${MUSL_TRIPLE} \
    -DCMAKE_CXX_FLAGS=${MUSL_RUNTIMES_FLAGS} \
    -DCMAKE_C_COMPILER=${CLANG_PREFIX}/bin/clang \
    -DCMAKE_C_COMPILER_TARGET=${MUSL_TRIPLE} \
    -DCMAKE_C_FLAGS=${MUSL_RUNTIMES_FLAGS} \
    -DCMAKE_EXE_LINKER_FLAGS=-fuse-ld=lld \
    -DCMAKE_INSTALL_PREFIX=${MUSL_SYSROOT} \
    -DCMAKE_NM=${CLANG_PREFIX}/bin/llvm-nm \
    -DCMAKE_RANLIB=${CLANG_PREFIX}/bin/llvm-ranlib \
    -DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
    -DLIBCXXABI_BAREMETAL=OFF \
    -DLIBCXXABI_ENABLE_ASSERTIONS=OFF \
    -DLIBCXXABI_ENABLE_SHARED=OFF \
    -DLIBCXXABI_ENABLE_STATIC=ON \
    -DLIBCXXABI_LIBCXX_INCLUDES=${MUSL_SYSROOT}/include/c++/v1 \
    -DLIBCXXABI_USE_COMPILER_RT=ON \
    -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
    -DLIBCXX_CXX_ABI=libcxxabi \
    -DLIBCXX_ENABLE_DEBUG_MODE_SUPPORT=OFF \
    -DLIBCXX_ENABLE_FILESYSTEM=OFF \
    -DLIBCXX_ENABLE_SHARED=OFF \
    -DLIBCXX_ENABLE_STATIC=ON \
    -DLIBCXX_INCLUDE_BENCHMARKS=OFF \
    -DLIBUNWIND_ENABLE_SHARED=OFF \
    -DLIBUNWIND_ENABLE_STATIC=ON \
    -DLIBUNWIND_IS_BAREMETAL=ON \
    -DLIBUNWIND_REMEMBER_HEAP_ALLOC=ON \
    -DLIBUNWIND_USE_COMPILER_RT=ON \
    -DLLVM_ENABLE_RUNTIMES=${RUNTIMES_TO_BUILD} \
    -DLIBCXXABI_ENABLE_EXCEPTIONS=OFF \
    -DLIBCXXABI_ENABLE_THREADS=OFF \
    -DLIBCXX_ENABLE_EXCEPTIONS=OFF \
    -DLIBCXX_ENABLE_MONOTONIC_CLOCK=OFF \
    -DLIBCXX_ENABLE_RANDOM_DEVICE=OFF \
    -DLIBCXX_ENABLE_RTTI=OFF \
    -DLIBCXX_ENABLE_THREADS=OFF \
    -DLIBCXX_ENABLE_WIDE_CHARACTERS=OFF \
    -DLIBCXX_EXTRA_SITE_DEFINES=_LIBCPP_PROVIDES_DEFAULT_RUNE_TABLE \
    -DLIBUNWIND_ENABLE_THREADS=OFF \
    $SRC_RUNTIMES
    '''

config_cmd = 'cmake \\' + config_args


def do_config():
    BUILD_RUNTIMES_MUSL.mkdir(parents=True, exist_ok=True)
    cmd1 = 'cd ' + BUILD_RUNTIMES_MUSL.as_posix()
    cmd2 = config_cmd
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def config_runtimes_musl():
    if not is_runtimes_musl_configured():
        ret = do_config()
        if ret != 0:
            print('runtimes for musl config failed')
            exit(1)
        runtimes_musl_configured()


def do_build_libcxx():
    cmd1 = 'cd ' + BUILD_RUNTIMES_MUSL.as_posix()
    cmd2 = 'ninja cxx'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def do_build_libcxxabi():
    cmd1 = 'cd ' + BUILD_RUNTIMES_MUSL.as_posix()
    cmd2 = 'ninja cxxabi'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def do_build_libunwind():
    cmd1 = 'cd ' + BUILD_RUNTIMES_MUSL.as_posix()
    cmd2 = 'ninja unwind'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def build_runtimes_musl():
    if not is_runtimes_musl_built():
        ret = do_build_libcxx()
        if ret != 0:
            print('libcxx for musl build failed')
            exit(1)
        ret = do_build_libcxxabi()
        if ret != 0:
            print('libcxxabi for musl build failed')
            exit(1)
        ret = do_build_libunwind()
        if ret != 0:
            print('libunwind for musl build failed')
            exit(1)
        runtimes_musl_built()


def do_install_libcxx():
    cmd1 = 'cd ' + BUILD_RUNTIMES_MUSL.as_posix()
    cmd2 = 'ninja install-cxx'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def do_install_libcxxabi():
    cmd1 = 'cd ' + BUILD_RUNTIMES_MUSL.as_posix()
    cmd2 = 'ninja install-cxxabi'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def do_install_libunwind():
    cmd1 = 'cd ' + BUILD_RUNTIMES_MUSL.as_posix()
    cmd2 = 'ninja install-unwind'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def install_runtimes_musl():
    if not is_runtimes_musl_installed():
        ret = do_install_libcxx()
        if ret != 0:
            print('libcxx for musl install failed')
            exit(1)
        ret = do_install_libcxxabi()
        if ret != 0:
            print('libcxxabi for musl install failed')
            exit(1)
        ret = do_install_libunwind()
        if ret != 0:
            print('libunwind for musl install failed')
            exit(1)
        runtimes_musl_installed()


def process_runtimes_musl():
    libc = get_libc_type()
    if libc != '-elf':
        config_runtimes_musl()
        build_runtimes_musl()
        install_runtimes_musl()
