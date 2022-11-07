from init_dir import init_dir
from preparation.download import download_tarballs
from preparation.git_clone import clone_code
from preparation.extract import extract_tarballs
from preparation.patch import patch_srouces
from process.clang import process_clang
from process.compier_rt_elf import process_compiler_rt_elf
from process.compier_rt_musl import process_compiler_rt_musl
from process.linux_headers import process_linux_headers
from process.musl_headers import process_musl_headers
from process.musl import process_musl
from process.newlib import process_newlib
from user_input import user_input


def main():
    user_input()
    init_dir()
    download_tarballs()
    clone_code()
    extract_tarballs()
    patch_srouces()

    process_clang()
    process_linux_headers()
    process_musl_headers()
    process_newlib()
    process_compiler_rt_elf()
    process_compiler_rt_musl()
    process_musl()


if __name__ == '__main__':
    main()
