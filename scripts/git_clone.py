from pathlib import Path

from git.repo import Repo

from scripts.config import LLVM_GIT_URL, LLVM_PROJ_NAME, SRC_ROOT
from scripts.record_step import clang_cloned, compiler_rt_elf_cloned, \
    compiler_rt_musl_cloned, is_clang_cloned, libcxx_cloned, libcxxabi_cloned, \
    libunwind_cloned


def git_clone(url, name):
    src_path = SRC_ROOT.joinpath(name)
    if src_path.exists():
        print(name + ' is already cloned')
        return
    try:
        print('Cloning ' + url + ' ...')
        Repo.clone_from(url=url, to_path=src_path)
        print(name + ' is cloned')
    except Exception as e:
        print(e)


def clone_code():
    if not is_clang_cloned():
        git_clone(LLVM_GIT_URL, LLVM_PROJ_NAME)
        clang_cloned()
        compiler_rt_elf_cloned()
        compiler_rt_musl_cloned()
        libcxx_cloned()
        libcxxabi_cloned()
        libunwind_cloned()
