from common.user_input import get_libc_type
from conf.conf import BUILD_NEWLIB
from utils.record_step import is_newlib_built, is_newlib_configured, \
    is_newlib_installed, newlib_built, newlib_configured, newlib_installed
from utils.run_shell import run_shell

config_args = \
    '''
    --prefix=$CLANG_PREFIX \
    --target=$NEWLIB_TRIPLE \
    --enable-newlib-io-long-double \
    --enable-newlib-io-long-long \
    --enable-newlib-io-c99-formats \
    --enable-newlib-register-fini \
    --disable-multilib \
    --disable-nls
    '''

config_cmd1 = 'export CFLAGS_FOR_TARGET=" -Wno-int-conversion -g -gdwarf-3 ' \
              '-gstrict-dwarf -O2 -ffunction-sections -fdata-sections "'
config_cmd2 = 'export CC_FOR_TARGET=$NEWLIB_TRIPLE-clang'
config_cmd3 = 'export AS_FOR_TARGET=$NEWLIB_TRIPLE-clang'
config_cmd4 = 'export LD_FOR_TARGET=lld'
config_cmd5 = 'export CXX_FOR_TARGET=$NEWLIB_TRIPLE-clang++'
config_cmd6 = 'export AR_FOR_TARGET=llvm-ar'
config_cmd7 = 'export NM_FOR_TARGET=llvm-nm'
config_cmd8 = 'export RANLIB_FOR_TARGET=llvm-ranlib'
config_cmd9 = 'export OBJCOPY_FOR_TARGET=llvm-objcopy'
config_cmd10 = 'export OBJDUMP_FOR_TARGET=llvm-objdump'
config_cmd11 = 'export READELF_FOR_TARGET=llvm-readelf'
config_cmd12 = 'export STRIP_FOR_TARGET=llvm-strip'
config_cmd13 = 'export LIPO_FOR_TARGET=llvm-lipo'
config_cmd14 = 'export DLLTOOL_FOR_TARGET=llvm-dlltool'
config_cmd15 = '$SRC_NEWLIB/configure \\' + config_args

config_cmd = config_cmd1 + '&&' + config_cmd2 + '&&' + config_cmd3 \
             + '&&' + config_cmd4 + '&&' + config_cmd5 + '&&' + config_cmd6 \
             + '&&' + config_cmd7 + '&&' + config_cmd8 + '&&' + config_cmd9 \
             + '&&' + config_cmd10 + '&&' + config_cmd11 + '&&' + config_cmd12 \
             + '&&' + config_cmd13 + '&&' + config_cmd14 + '&&' + config_cmd15


def do_config():
    BUILD_NEWLIB.mkdir(parents=True, exist_ok=True)
    cmd1 = 'cd ' + BUILD_NEWLIB.as_posix()
    cmd2 = config_cmd
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def config_newlib():
    if not is_newlib_configured():
        ret = do_config()
        if ret != 0:
            print('newlib config failed')
            exit(1)
        newlib_configured()


def do_build():
    cmd1 = 'cd ' + BUILD_NEWLIB.as_posix()
    cmd2 = 'make $JOBS all'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def build_newlib():
    if not is_newlib_built():
        ret = do_build()
        if ret != 0:
            print('newlib build failed')
            exit(1)
        newlib_built()


def do_install():
    cmd1 = 'cd ' + BUILD_NEWLIB.as_posix()
    cmd2 = 'make install'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def install_newlib():
    if not is_newlib_installed():
        ret = do_install()
        if ret != 0:
            print('newlib install failed')
            exit(1)
        newlib_installed()


def process_newlib():
    libc = get_libc_type()
    if libc != '-linux-musl':
        config_newlib()
        build_newlib()
        install_newlib()
