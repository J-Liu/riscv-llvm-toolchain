import platform

from conf.conf import BUILD_QEMU
from utils.record_step import is_qemu_built, is_qemu_configured, \
    is_qemu_installed, qemu_built, qemu_configured, qemu_installed
from utils.run_shell import run_shell

config_args = ''
if platform.system() == 'Linux':
    config_args = \
        '''
        --prefix=$CLANG_PREFIX \
        --target-list=riscv64-softmmu,riscv64-linux-user
        '''
else:
    config_args = \
        '''
        --prefix=$CLANG_PREFIX \
        --target-list=riscv64-softmmu
        '''

config_cmd = '$SRC_QEMU/configure \\' + config_args


def do_config():
    BUILD_QEMU.mkdir(parents=True, exist_ok=True)
    cmd1 = 'cd ' + BUILD_QEMU.as_posix()
    cmd2 = config_cmd
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def config_qemu():
    if not is_qemu_configured():
        ret = do_config()
        if ret != 0:
            print('qemu config failed')
            exit(1)
        qemu_configured()


def do_build():
    cmd1 = 'cd ' + BUILD_QEMU.as_posix()
    cmd2 = 'make $JOBS all'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def build_qemu():
    if not is_qemu_built():
        ret = do_build()
        if ret != 0:
            print('qemu build failed')
            exit(1)
        qemu_built()


def do_install():
    cmd1 = 'cd ' + BUILD_QEMU.as_posix()
    cmd2 = 'make install'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def install_qemu():
    if not is_qemu_installed():
        ret = do_install()
        if ret != 0:
            print('qemu install failed')
            exit(1)
        qemu_installed()


def process_qemu():
    config_qemu()
    build_qemu()
    install_qemu()
