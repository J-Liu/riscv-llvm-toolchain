from scripts.clang import process_clang
from scripts.compier_rt_elf import process_compiler_rt_elf
from scripts.compier_rt_musl import process_compiler_rt_musl
from scripts.download import download_tarballs
from scripts.git_clone import clone_code
from scripts.init_dir import init_dir
from scripts.linux_headers import process_linux_headers
from scripts.musl_headers import process_musl_headers
from scripts.musl import process_musl
from scripts.newlib import process_newlib
from scripts.user_input import user_input


def main():
    user_input()
    init_dir()
    download_tarballs()
    clone_code()

    process_clang()
    process_linux_headers()
    process_musl_headers()
    process_newlib()
    process_compiler_rt_elf()
    process_compiler_rt_musl()
    process_musl()


if __name__ == '__main__':
    main()
