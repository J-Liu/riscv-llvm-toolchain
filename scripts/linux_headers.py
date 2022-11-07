from scripts.conf import SRC_LINUX
from scripts.record_step import is_linux_headers_configured, \
    is_linux_headers_installed, linux_headers_configured, \
    linux_headers_installed
from scripts.run_shell import run_shell
from scripts.user_input import get_libc_type


def do_config():
    cmd1 = 'cd ' + SRC_LINUX.as_posix()
    cmd2 = 'make ARCH=riscv CROSS_COMPILE=$MUSL_TRIPLE- defconfig'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def config_linux():
    if not is_linux_headers_configured():
        ret = do_config()
        if ret != 0:
            print('linux config failed')
            exit(1)
        linux_headers_configured()


def do_install():
    cmd1 = 'cd ' + SRC_LINUX.as_posix()
    cmd2 = 'make ARCH=riscv INSTALL_HDR_PATH=$MUSL_SYSROOT/usr headers_install'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def install_linux_headers():
    if not is_linux_headers_installed():
        ret = do_install()
        if ret != 0:
            print('linux-headers install failed')
            exit(1)
        linux_headers_installed()


def process_linux_headers():
    libc = get_libc_type()
    if libc != '-elf':
        config_linux()
        install_linux_headers()
