from scripts.conf import BUILD_MUSL_HEADERS
from scripts.record_step import is_musl_headers_configured, \
    is_musl_headers_installed, musl_headers_configured, \
    musl_headers_installed
from scripts.run_shell import run_shell
from scripts.user_input import get_libc_type

config_args = \
    '''
    --host=$TARGET_TRIPLE \
    --prefix=$MUSL_SYSROOT/usr \
    --enable-shared \
    --with-headers=$MUSL_SYSROOT/usr/include \
    --disable-multilib \
    --enable-kernel=3.0.0
    '''


def do_config():
    BUILD_MUSL_HEADERS.mkdir(parents=True, exist_ok=True)
    cmd1 = 'cd ' + BUILD_MUSL_HEADERS.as_posix()
    cmd2 = '$SRC_MUSL/configure ' + config_args
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def config_musl():
    if not is_musl_headers_configured():
        ret = do_config()
        if ret != 0:
            print('musl-headers config failed')
            exit(1)
        musl_headers_configured()


def do_install():
    cmd1 = 'cd ' + BUILD_MUSL_HEADERS.as_posix()
    cmd2 = 'make install-headers'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def install_musl_headers():
    if not is_musl_headers_installed():
        ret = do_install()
        if ret != 0:
            print('musl-headers install failed')
            exit(1)
        musl_headers_installed()


def process_musl_headers():
    libc = get_libc_type()
    if libc != '-elf':
        config_musl()
        install_musl_headers()
