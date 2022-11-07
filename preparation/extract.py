from conf.conf import LINUX_TARBALL, MUSL_TARBALL, NEWLIB_TARBALL, \
    SRC_LINUX, SRC_MUSL, SRC_NEWLIB
from utils.record_step import is_linux_headers_extracted, \
    is_musl_extracted, is_newlib_extracted, linux_headers_extracted, \
    musl_extracted, musl_headers_extracted, newlib_extracted
from utils.run_shell import run_shell


def extract_tarball(tarball):
    cmd1 = 'cd $SRC_ROOT'
    cmd2 = 'tar vxf $TARBALL_ROOT/' + tarball
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def extract_linux():
    if not is_linux_headers_extracted():
        if SRC_LINUX.exists():
            print(SRC_LINUX.as_posix() + ' is already exists')
            linux_headers_extracted()
            return
        ret = extract_tarball(LINUX_TARBALL)
        if ret != 0:
            print(LINUX_TARBALL + ' is broken')
            exit(1)
        linux_headers_extracted()


def extract_musl():
    if not is_musl_extracted():
        if SRC_MUSL.exists():
            print(SRC_MUSL.as_posix() + ' is already exists')
            musl_extracted()
            musl_headers_extracted()
            return
        ret = extract_tarball(MUSL_TARBALL)
        if ret != 0:
            print(MUSL_TARBALL + ' is broken')
            exit(1)
        musl_extracted()
        musl_headers_extracted()


def extract_newlib():
    if not is_newlib_extracted():
        if SRC_NEWLIB.exists():
            print(SRC_NEWLIB.as_posix() + ' is already exists')
            newlib_extracted()
            return
        ret = extract_tarball(NEWLIB_TARBALL)
        if ret != 0:
            print(NEWLIB_TARBALL + ' is broken')
            exit(1)
        newlib_extracted()


def extract_tarballs():
    extract_linux()
    extract_musl()
    extract_newlib()


if __name__ == '__main__':
    from conf.environment import init_env

    init_env()
    extract_tarballs()
