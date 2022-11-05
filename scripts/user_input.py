import json

from pathlib import Path

from scripts.config import TOP_PATH

conf_path = TOP_PATH.joinpath('conf').with_suffix('.json')


class BoldColor:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BOLD_UNDERLINE = '\033[1;4m'
    END = '\033[0m'


def user_input():
    libc_type = input(BoldColor.BOLD_UNDERLINE + '[0:all' + BoldColor.END +
                      '(Default), 1:newlib, 2:musl]:')
    if libc_type == '0' or libc_type.isspace() or len(libc_type) == 0:
        libc = ''
    elif libc_type == '1':
        libc = '-elf'
    elif libc_type == '2':
        libc = '-linux-musl'
    else:
        print(BoldColor.RED + 'Please choose right libc type' + BoldColor.END)
        exit(1)

    build_type = input(BoldColor.BOLD_UNDERLINE + '[0:Release' +
                       BoldColor.END + '(Default), 1:Debug]:')
    build = 'Release'
    if build_type == '0' or build_type.isspace() or len(build_type) == 0:
        build = 'Release'
    elif build_type == '1':
        build = 'Debug'
    else:
        print(BoldColor.RED + 'Please choose right build type' + BoldColor.END)
        exit(1)

    toolchain_name = 'riscv' + libc + '-clang'
    default_install_path = TOP_PATH.parent.joinpath(toolchain_name)
    default_install_path_str = '[prefix:' + BoldColor.BOLD_UNDERLINE + \
                               default_install_path.as_posix() + BoldColor.END + \
                               '(Default)]:'
    install_path = input(default_install_path_str)
    path = default_install_path
    if install_path.isspace() or len(install_path) == 0:
        path = default_install_path
    else:
        path = Path(install_path)

    try:
        path.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(
            BoldColor.RED + 'PREFIX is already exist, please type another one' +
            BoldColor.END)
        # exit(1)
    except Exception as e:
        print(BoldColor.YELLOW + repr(e) + BoldColor.END)
        print(BoldColor.RED + 'Make sure your PREFIX is right or accessible' +
              BoldColor.END)
        exit(1)

    obj = {
        'libc': libc,
        'build': build,
        'prefix': path.as_posix()
    }

    with conf_path.open('w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)
