from scripts.config import PATCH_NEWLIB_C99, SRC_NEWLIB
from scripts.record_step import is_newlib_patched, newlib_patched
from scripts.run_shell import run_shell


def patch_src(src, patch):
    cmd1 = 'cd ' + src.as_posix()
    cmd2 = 'patch -p1 < ' + patch.as_posix()
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def patch_newlib():
    if not is_newlib_patched():
        ret = patch_src(SRC_NEWLIB, PATCH_NEWLIB_C99)
        if ret != 0:
            print(SRC_NEWLIB.as_posix() + ' patch failed')
            exit(1)
        newlib_patched()


if __name__ == '__main__':
    from scripts.environment import init_env

    init_env()
    patch_newlib()
