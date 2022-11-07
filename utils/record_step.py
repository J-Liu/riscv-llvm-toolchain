import json

from conf.conf import TOP_PATH

step_path = TOP_PATH.joinpath('step').with_suffix('.json')


def reset_steps():
    clang = {
        'git': False,
        'config': False,
        'build': False,
        'install': False,
        'post-config-elf': False,
        'post-config-musl': False
    }
    linux_headers = {
        'download': False,
        'extract': False,
        'config': False,
        'install': False
    }
    newlib = {
        'download': False,
        'extract': False,
        'patch': False,
        'config': False,
        'build': False,
        'install': False
    }
    musl_headers = {
        'download': False,
        'extract': False,
        'config': False,
        'install': False
    }
    compiler_rt_elf = {
        'git': False,
        'config': False,
        'build': False,
        'install': False
    }
    compiler_rt_musl = {
        'git': False,
        'config': False,
        'build': False,
        'install': False
    }
    musl = {
        'download': False,
        'extract': False,
        'config': False,
        'build': False,
        'install': False
    }
    libunwind = {
        'git': False,
        'config': False,
        'build': False,
        'install': False
    }
    libcxx = {
        'git': False,
        'config': False,
        'build': False,
        'install': False
    }
    libcxxabi = {
        'git': False,
        'config': False,
        'build': False,
        'install': False
    }

    progress = {
        'clang': clang,
        'linux-headers': linux_headers,
        'newlib': newlib,
        'musl-headers': musl_headers,
        'compiler-rt-elf': compiler_rt_elf,
        'compiler-rt-musl': compiler_rt_musl,
        'musl': musl,
        'libunwind': libunwind,
        'libcxx': libcxx,
        'libcxxabi': libcxxabi
    }

    with step_path.open('w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)


def load_key(key, subkey):
    with step_path.open('r', encoding='utf-8') as f:
        obj = json.load(f)
        item = obj.get(key)
        v = item.get(subkey)
        return v


def store_key(key, subkey, value):
    with step_path.open('r', encoding='utf-8') as f:
        obj = json.load(f)
        item = obj.get(key)
        item[subkey] = value
    with step_path.open('w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)


def is_done(key, subkey):
    if load_key(key, subkey):
        return True
    return False


def is_clang_cloned():
    return is_done('clang', 'git')


def is_clang_configured():
    return is_done('clang', 'config')


def is_clang_built():
    return is_done('clang', 'build')


def is_clang_installed():
    return is_done('clang', 'install')


def is_clang_post_configured_elf():
    return is_done('clang', 'post-config-elf')


def is_clang_post_configured_musl():
    return is_done('clang', 'post-config-musl')


def is_linux_headers_downloaded():
    return is_done('linux-headers', 'download')


def is_linux_headers_extracted():
    return is_done('linux-headers', 'extract')


def is_linux_headers_configured():
    return is_done('linux-headers', 'config')


def is_linux_headers_installed():
    return is_done('linux-headers', 'install')


def is_newlib_downloaded():
    return is_done('newlib', 'download')


def is_newlib_extracted():
    return is_done('newlib', 'extract')


def is_newlib_patched():
    return is_done('newlib', 'patch')


def is_newlib_configured():
    return is_done('newlib', 'config')


def is_newlib_built():
    return is_done('newlib', 'build')


def is_newlib_installed():
    return is_done('newlib', 'install')


def is_musl_headers_downloaded():
    return is_done('musl-headers', 'download')


def is_musl_headers_extracted():
    return is_done('musl-headers', 'extract')


def is_musl_headers_configured():
    return is_done('musl-headers', 'config')


def is_musl_headers_installed():
    return is_done('musl-headers', 'install')


def is_compiler_rt_elf_cloned():
    return is_done('compiler-rt-elf', 'git')


def is_compiler_rt_elf_configured():
    return is_done('compiler-rt-elf', 'config')


def is_compiler_rt_elf_built():
    return is_done('compiler-rt-elf', 'build')


def is_compiler_rt_elf_installed():
    return is_done('compiler-rt-elf', 'install')


def is_compiler_rt_musl_cloned():
    return is_done('compiler-rt-musl', 'git')


def is_compiler_rt_musl_configured():
    return is_done('compiler-rt-musl', 'config')


def is_compiler_rt_musl_built():
    return is_done('compiler-rt-musl', 'build')


def is_compiler_rt_musl_installed():
    return is_done('compiler-rt-musl', 'install')


def is_musl_downloaded():
    return is_done('musl', 'download')


def is_musl_extracted():
    return is_done('musl', 'extract')


def is_musl_configured():
    return is_done('musl', 'config')


def is_musl_built():
    return is_done('musl', 'build')


def is_musl_installed():
    return is_done('musl', 'install')


def is_libunwind_cloned():
    return is_done('libunwind', 'git')


def is_libunwind_configured():
    return is_done('libunwind', 'config')


def is_libunwind_built():
    return is_done('libunwind', 'build')


def is_libunwind_installed():
    return is_done('libunwind', 'install')


def is_libcxx_cloned():
    return is_done('libcxx', 'git')


def is_libcxx_configured():
    return is_done('libcxx', 'config')


def is_libcxx_built():
    return is_done('libcxx', 'build')


def is_libcxx_installed():
    return is_done('libcxx', 'install')


def is_libcxxabi_cloned():
    return is_done('libcxxabi', 'git')


def is_libcxxabi_configured():
    return is_done('libcxxabi', 'config')


def is_libcxxabi_built():
    return is_done('libcxxabi', 'build')


def is_libcxxabi_installed():
    return is_done('libcxxabi', 'install')


def done(key, subkey):
    store_key(key, subkey, True)


def clang_cloned():
    return done('clang', 'git')


def clang_configured():
    return done('clang', 'config')


def clang_built():
    return done('clang', 'build')


def clang_installed():
    return done('clang', 'install')


def clang_post_configured_elf():
    return done('clang', 'post-config-elf')


def clang_post_configured_musl():
    return done('clang', 'post-config-musl')


def linux_headers_downloaded():
    return done('linux-headers', 'download')


def linux_headers_extracted():
    return done('linux-headers', 'extract')


def linux_headers_configured():
    return done('linux-headers', 'config')


def linux_headers_installed():
    return done('linux-headers', 'install')


def newlib_downloaded():
    return done('newlib', 'download')


def newlib_extracted():
    return done('newlib', 'extract')


def newlib_patched():
    return done('newlib', 'patch')


def newlib_configured():
    return done('newlib', 'config')


def newlib_built():
    return done('newlib', 'build')


def newlib_installed():
    return done('newlib', 'install')


def musl_headers_downloaded():
    return done('musl-headers', 'download')


def musl_headers_extracted():
    return done('musl-headers', 'extract')


def musl_headers_configured():
    return done('musl-headers', 'config')


def musl_headers_installed():
    return done('musl-headers', 'install')


def compiler_rt_elf_cloned():
    return done('compiler-rt-elf', 'git')


def compiler_rt_elf_configured():
    return done('compiler-rt-elf', 'config')


def compiler_rt_elf_built():
    return done('compiler-rt-elf', 'build')


def compiler_rt_elf_installed():
    return done('compiler-rt-elf', 'install')


def compiler_rt_musl_cloned():
    return done('compiler-rt-musl', 'git')


def compiler_rt_musl_configured():
    return done('compiler-rt-musl', 'config')


def compiler_rt_musl_built():
    return done('compiler-rt-musl', 'build')


def compiler_rt_musl_installed():
    return done('compiler-rt-musl', 'install')


def musl_downloaded():
    return done('musl', 'download')


def musl_extracted():
    return done('musl', 'extract')


def musl_configured():
    return done('musl', 'config')


def musl_built():
    return done('musl', 'build')


def musl_installed():
    return done('musl', 'install')


def libunwind_cloned():
    return done('libunwind', 'git')


def libunwind_configured():
    return done('libunwind', 'config')


def libunwind_built():
    return done('libunwind', 'build')


def libunwind_installed():
    return done('libunwind', 'install')


def libcxx_cloned():
    return done('libcxx', 'git')


def libcxx_configured():
    return done('libcxx', 'config')


def libcxx_built():
    return done('libcxx', 'build')


def libcxx_installed():
    return done('libcxx', 'install')


def libcxxabi_cloned():
    return done('libcxxabi', 'git')


def libcxxabi_configured():
    return done('libcxxabi', 'config')


def libcxxabi_built():
    return done('libcxxabi', 'build')


def libcxxabi_installed():
    return done('libcxxabi', 'install')


if __name__ == '__main__':
    reset_steps()
