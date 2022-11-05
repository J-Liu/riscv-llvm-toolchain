from pathlib import Path

from git.repo import Repo

from scripts.config import SRC_ROOT
from scripts.record_step import store_key, load_key


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
    llvm_git_url = 'https://github.com/llvm/llvm-project.git'
    llvm_name = 'llvm-project'
    if not load_key('clang', 'git'):
        git_clone(llvm_git_url, llvm_name)
        store_key('clang', 'git', True)
        store_key('compiler-rt', 'git', True)
        store_key('libunwind', 'git', True)
        store_key('libcxx', 'git', True)
        store_key('libcxxabi', 'git', True)
