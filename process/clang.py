import os
import stat

from pathlib import Path

from common.user_input import get_libc_type
from conf import BUILD_CLANG, CLANG_TEMPLATE, MUSL_TRIPLE, \
    NEWLIB_TRIPLE
from utils.record_step import clang_built, clang_configured, \
    clang_installed, clang_post_configured_elf, clang_post_configured_musl, \
    is_clang_built, is_clang_configured, is_clang_installed, \
    is_clang_post_configured_elf, is_clang_post_configured_musl
from utils.run_shell import run_shell

config_args = \
    '''
    -G Ninja \
    -DLLVM_ENABLE_PROJECTS=$TOOLS_TO_BUILD \
    -DCMAKE_BUILD_TYPE=$BUILE_TYPE \
    -DCMAKE_INSTALL_PREFIX=$CLANG_PREFIX \
    -DLLVM_TARGETS_TO_BUILD=$TARGETS_TO_BUILD \
    -DLLVM_BUILD_EXAMPLES=OFF \
    -DLLVM_INCLUDE_EXAMPLES=OFF \
    -DBUILD_SHARED_LIBS=OFF \
    -DLLVM_OPTIMIZED_TABLEGEN=ON \
    -DLLVM_ENABLE_LIBXML2=OFF \
    -DCLANG_ENABLE_ARCMT=OFF \
    -DCLANG_ENABLE_STATIC_ANALYZER=OFF \
    -DCLANG_DEFAULT_RTLIB=compiler-rt \
    $SRC_LLVM
    '''

link_cmd1 = 'cd $CLANG_PREFIX/bin'
musl_link_cmd2 = 'ln -s $MUSL_TRIPLE-clang $MUSL_TRIPLE-gcc'
musl_link_cmd3 = 'ln -s $MUSL_TRIPLE-clang++ $MUSL_TRIPLE-g++'
musl_link_cmd4 = 'ln -s lld $MUSL_TRIPLE-ld'
musl_link_cmd5 = 'ln -s lld $MUSL_TRIPLE-ld.lld'
musl_link_cmd6 = 'ln -s lld $MUSL_TRIPLE-ld64.lld'
musl_link_cmd7 = 'ln -s lld $MUSL_TRIPLE-ld.bfd'
musl_link_cmd8 = 'ln -s lld $MUSL_TRIPLE-ld.gold'
musl_link_cmd9 = 'ln -s llvm-ar $MUSL_TRIPLE-ar'
musl_link_cmd10 = 'ln -s llvm-nm $MUSL_TRIPLE-nm'
musl_link_cmd11 = 'ln -s llvm-objcopy $MUSL_TRIPLE-objcopy'
musl_link_cmd12 = 'ln -s llvm-objdump $MUSL_TRIPLE-objdump'
musl_link_cmd13 = 'ln -s llvm-ranlib $MUSL_TRIPLE-ranlib'
musl_link_cmd14 = 'ln -s llvm-strip $MUSL_TRIPLE-strip'

musl_link_cmd = link_cmd1 + ' && ' + musl_link_cmd2 + ' && ' + musl_link_cmd3 \
                + ' && ' + musl_link_cmd4 + ' && ' + musl_link_cmd5 \
                + ' && ' + musl_link_cmd6 + ' && ' + musl_link_cmd7 \
                + ' && ' + musl_link_cmd8 + ' && ' + musl_link_cmd9 \
                + ' && ' + musl_link_cmd10 + ' && ' + musl_link_cmd11 \
                + ' && ' + musl_link_cmd12 + ' && ' + musl_link_cmd13 \
                + ' && ' + musl_link_cmd14

newlib_link_cmd2 = 'ln -s $NEWLIB_TRIPLE-clang $NEWLIB_TRIPLE-gcc'
newlib_link_cmd3 = 'ln -s $NEWLIB_TRIPLE-clang++ $NEWLIB_TRIPLE-g++'
newlib_link_cmd4 = 'ln -s lld $NEWLIB_TRIPLE-ld'
newlib_link_cmd5 = 'ln -s lld $NEWLIB_TRIPLE-ld.lld'
newlib_link_cmd6 = 'ln -s lld $NEWLIB_TRIPLE-ld64.lld'
newlib_link_cmd7 = 'ln -s lld $NEWLIB_TRIPLE-ld.bfd'
newlib_link_cmd8 = 'ln -s lld $NEWLIB_TRIPLE-ld.gold'
newlib_link_cmd9 = 'ln -s llvm-ar $NEWLIB_TRIPLE-ar'
newlib_link_cmd10 = 'ln -s llvm-nm $NEWLIB_TRIPLE-nm'
newlib_link_cmd11 = 'ln -s llvm-objcopy $NEWLIB_TRIPLE-objcopy'
newlib_link_cmd12 = 'ln -s llvm-objdump $NEWLIB_TRIPLE-objdump'
newlib_link_cmd13 = 'ln -s llvm-ranlib $NEWLIB_TRIPLE-ranlib'
newlib_link_cmd14 = 'ln -s llvm-strip $NEWLIB_TRIPLE-strip'

newlib_link_cmd = link_cmd1 + ' && ' + newlib_link_cmd2 \
                  + ' && ' + newlib_link_cmd3 + ' && ' + newlib_link_cmd4 \
                  + ' && ' + newlib_link_cmd5 + ' && ' + newlib_link_cmd6 \
                  + ' && ' + newlib_link_cmd7 + ' && ' + newlib_link_cmd8 \
                  + ' && ' + newlib_link_cmd9 + ' && ' + newlib_link_cmd10 \
                  + ' && ' + newlib_link_cmd11 + ' && ' + newlib_link_cmd12 \
                  + ' && ' + newlib_link_cmd13 + ' && ' + newlib_link_cmd14


def do_config():
    BUILD_CLANG.mkdir(parents=True, exist_ok=True)
    cmd1 = 'cd ' + BUILD_CLANG.as_posix()
    cmd2 = 'cmake ' + config_args
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def config_clang():
    if not is_clang_configured():
        ret = do_config()
        if ret != 0:
            print('clang config failed')
            exit(1)
        clang_configured()


def do_build():
    cmd1 = 'cd ' + BUILD_CLANG.as_posix()
    cmd2 = 'ninja'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def build_clang():
    if not is_clang_built():
        ret = do_build()
        if ret != 0:
            print('clang build failed')
            exit(1)
        clang_built()


def do_install():
    cmd1 = 'cd ' + BUILD_CLANG.as_posix()
    cmd2 = 'ninja install'
    cmd = cmd1 + ' && ' + cmd2
    ret = run_shell(cmd)
    return ret


def install_clang():
    if not is_clang_installed():
        ret = do_install()
        if ret != 0:
            print('clang install failed')
            exit(1)
        clang_installed()


def do_alias(template, alias, prefix, name, target, sysroot):
    with open(template, 'r') as f:
        x = f.read()
    with open(alias, 'w') as f:
        x = x.replace('PREFIX', prefix)
        x = x.replace('CLANG', name)
        x = x.replace('TARGET', target)
        x = x.replace('SYSROOT', sysroot)
        f.write(x)
    f = Path(alias)
    f.chmod(f.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def make_alias(target, sysroot):
    template = CLANG_TEMPLATE.as_posix()
    prefix = os.environ.get('CLANG_PREFIX')
    target = target
    cc_alias = prefix + '/bin/' + target + '-clang'
    cxx_alias = prefix + '/bin/' + target + '-clang++'
    sysroot = sysroot
    do_alias(template, cc_alias, prefix, 'clang', target, sysroot)
    do_alias(template, cxx_alias, prefix, 'clang++', target, sysroot)


def alias_musl_clang():
    target = MUSL_TRIPLE
    sysroot = os.environ.get('MUSL_SYSROOT')
    make_alias(target, sysroot)


def alias_newlib_clang():
    target = NEWLIB_TRIPLE
    sysroot = os.environ.get('NEWLIB_SYSROOT')
    make_alias(target, sysroot)


def do_post_config_elf():
    ret = run_shell(newlib_link_cmd)
    return ret


def post_config_clang_elf():
    if not is_clang_post_configured_elf():
        ret = do_post_config_elf()
        if ret != 0:
            print('newlib clang post config failed')
            exit(1)
        clang_post_configured_elf()


def do_post_config_musl():
    alias_musl_clang()
    ret = run_shell(musl_link_cmd)
    return ret


def post_config_clang_musl():
    if not is_clang_post_configured_musl():
        ret = do_post_config_musl()
        if ret != 0:
            print('musl clang post config failed')
            exit(1)
        clang_post_configured_musl()


def post_config_clang():
    libc = get_libc_type()
    if libc == '-elf':
        alias_newlib_clang()
        post_config_clang_elf()
    elif libc == '-linux-musl':
        alias_musl_clang()
        post_config_clang_musl()
    else:
        alias_musl_clang()
        alias_newlib_clang()
        post_config_clang_elf()
        post_config_clang_musl()


def process_clang():
    config_clang()
    build_clang()
    install_clang()
    post_config_clang()


if __name__ == '__main__':
    from environment import init_env

    init_env()
    process_clang()
