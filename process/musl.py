from common.user_input import get_libc_type
from conf.conf import BUILD_MUSL
from utils.record_step import is_musl_built, is_musl_configured, \
    is_musl_installed, musl_built, musl_configured, musl_installed
from utils.run_shell import run_shell

pre_config_args = \
    '''
    CC=$MUSL_TRIPLE-clang \
    CXX=$MUSL_TRIPLE-clang++ \
    CFLAGS="$MUSL_CFLAGS -g -O2" \
    CXXFLAGS="$MUSL_CXXFLAGS -g -O2" \
    ASFLAGS=$MUSL_CFLAGS \
    CROSS_COMPILE=$MUSL_TRIPLE- \
    LIBCC=$COMPILER_RT_INSTALL/lib/linux/libclang_rt.builtins-riscv64.a \
    '''

config_args = \
    '''
    --host=$MUSL_TRIPLE \
    --prefix=$MUSL_SYSROOT \
    --disable-werror \
    --enable-shared
    '''

config_cmd1 = 'export LLVM_VERSION=`clang -dumpversion`'
config_cmd2 = 'export LLVM_RESOURCEDIR=lib/clang/$LLVM_VERSION'
config_cmd3 = 'export COMPILER_RT_INSTALL=$CLANG_PREFIX/$LLVM_RESOURCEDIR'
config_cmd4 = pre_config_args + ' $SRC_MUSL/configure \\' + config_args

config_cmd = config_cmd1 + '&&' + config_cmd2 + '&&' + config_cmd3 \
             + '&&' + config_cmd4


def do_config():
    BUILD_MUSL.mkdir(parents=True, exist_ok=True)
    cmd1 = 'cd ' + BUILD_MUSL.as_posix()
    cmd2 = config_cmd
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def config_musl():
    if not is_musl_configured():
        ret = do_config()
        if ret != 0:
            print('musl config failed')
            exit(1)
        musl_configured()


def do_build():
    cmd1 = 'cd ' + BUILD_MUSL.as_posix()
    cmd2 = 'make $JOBS'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def build_musl():
    if not is_musl_built():
        ret = do_build()
        if ret != 0:
            print('musl build failed')
            exit(1)
        musl_built()


def do_install():
    cmd1 = 'cd ' + BUILD_MUSL.as_posix()
    cmd2 = 'make install'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def install_musl():
    if not is_musl_installed():
        ret = do_install()
        if ret != 0:
            print('musl install failed')
            exit(1)
        musl_installed()


def process_musl():
    libc = get_libc_type()
    if libc != '-elf':
        config_musl()
        build_musl()
        install_musl()
