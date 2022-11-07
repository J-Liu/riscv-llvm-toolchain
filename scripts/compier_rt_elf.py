from scripts.config import BUILD_COMPILER_RT_NEWLIB
from scripts.record_step import compiler_rt_elf_built, \
    compiler_rt_elf_configured, compiler_rt_elf_installed, \
    is_compiler_rt_elf_built, is_compiler_rt_elf_configured, \
    is_compiler_rt_elf_installed
from scripts.run_shell import run_shell
from scripts.user_input import get_libc_type

config_args = \
    '''
    -G Ninja \
    -DCMAKE_INSTALL_PREFIX=$COMPILER_RT_INSTALL \
    -DCMAKE_BUILD_TYPE=$BUILE_TYPE \
    -DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
    -DCMAKE_CROSSCOMPILING=True \
    -DCMAKE_SYSTEM_NAME=Linux \
    -DCOMPILER_RT_BUILD_BUILTINS=ON \
    -DCOMPILER_RT_INCLUDE_TESTS=OFF \
    -DCOMPILER_RT_BUILD_CRT=ON \
    -DCOMPILER_RT_BUILD_SANITIZERS=OFF \
    -DCOMPILER_RT_BUILD_XRAY=OFF \
    -DCOMPILER_RT_BUILD_LIBFUZZER=OFF \
    -DCOMPILER_RT_BUILD_PROFILE=OFF \
    -DCOMPILER_RT_BUILD_MEMPROF=OFF \
    -DCOMPILER_RT_BUILD_ORC=OFF \
    -DCOMPILER_RT_DEFAULT_TARGET_ONLY=ON \
    -DCOMPILER_RT_BUILD_XRAY_NO_PREINIT=OFF \
    -DCOMPILER_RT_SANITIZERS_TO_BUILD=none \
    -DCOMPILER_RT_BAREMETAL_BUILD=ON \
    -DCOMPILER_RT_OS_DIR="" \
    -DCMAKE_ASM_COMPILER=clang \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_ASM_COMPILER_TARGET=$NEWLIB_TRIPLE \
    -DCMAKE_C_COMPILER_TARGET=$NEWLIB_TRIPLE \
    -DCMAKE_CXX_COMPILER_TARGET=$NEWLIB_TRIPLE \
    -DCMAKE_SYSROOT=$NEWLIB_SYSROOT \
    $SRC_COMPILER_RT
    '''

config_cmd1 = 'export LLVM_VERSION=`clang -dumpversion`'
config_cmd2 = 'export LLVM_RESOURCEDIR=lib/clang/$LLVM_VERSION'
config_cmd3 = 'export COMPILER_RT_INSTALL=$CLANG_PREFIX/$LLVM_RESOURCEDIR'
config_cmd4 = 'cmake ' + config_args

config_cmd = config_cmd1 + '&&' + config_cmd2 + '&&' + config_cmd3 \
             + '&&' + config_cmd4


def do_config():
    BUILD_COMPILER_RT_NEWLIB.mkdir(parents=True, exist_ok=True)
    cmd1 = 'cd ' + BUILD_COMPILER_RT_NEWLIB.as_posix()
    cmd2 = config_cmd
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def config_compiler_rt_elf():
    if not is_compiler_rt_elf_configured():
        ret = do_config()
        if ret != 0:
            print('compiler-rt for newlib config failed')
            exit(1)
        compiler_rt_elf_configured()


def do_build():
    cmd1 = 'cd ' + BUILD_COMPILER_RT_NEWLIB.as_posix()
    cmd2 = 'ninja'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def build_compiler_rt_elf():
    if not is_compiler_rt_elf_built():
        ret = do_build()
        if ret != 0:
            print('compiler-rt for newlib build failed')
            exit(1)
        compiler_rt_elf_built()


def do_install():
    cmd1 = 'cd ' + BUILD_COMPILER_RT_NEWLIB.as_posix()
    cmd2 = 'ninja install'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def install_compiler_rt_elf():
    if not is_compiler_rt_elf_installed():
        ret = do_install()
        if ret != 0:
            print('compiler-rt for newlib install failed')
            exit(1)
        compiler_rt_elf_installed()


def process_compiler_rt_elf():
    libc = get_libc_type()
    if libc != '-linux-musl':
        config_compiler_rt_elf()
        build_compiler_rt_elf()
        install_compiler_rt_elf()
