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
        'config': False,
        'build': False,
        'install': False
    }
    compiler_rt_musl = {
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
    runtimes_elf = {
        'config': False,
        'build': False,
        'install': False
    }
    runtimes_musl = {
        'config': False,
        'build': False,
        'install': False
    }
    qemu = {
        'download': False,
        'extract': False,
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
        'runtimes-elf': runtimes_elf,
        'runtimes-musl': runtimes_musl,
        'qemu': qemu
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


def is_compiler_rt_elf_configured():
    return is_done('compiler-rt-elf', 'config')


def is_compiler_rt_elf_built():
    return is_done('compiler-rt-elf', 'build')


def is_compiler_rt_elf_installed():
    return is_done('compiler-rt-elf', 'install')


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


def is_runtimes_elf_configured():
    return is_done('runtimes-elf', 'config')


def is_runtimes_elf_built():
    return is_done('runtimes-elf', 'build')


def is_runtimes_elf_installed():
    return is_done('runtimes-elf', 'install')


def is_runtimes_musl_configured():
    return is_done('runtimes-musl', 'config')


def is_runtimes_musl_built():
    return is_done('runtimes-musl', 'build')


def is_runtimes_musl_installed():
    return is_done('runtimes-musl', 'install')


def is_qemu_downloaded():
    return is_done('qemu', 'download')


def is_qemu_extracted():
    return is_done('qemu', 'extract')


def is_qemu_configured():
    return is_done('qemu', 'config')


def is_qemu_built():
    return is_done('qemu', 'build')


def is_qemu_installed():
    return is_done('qemu', 'install')


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




def compiler_rt_elf_configured():
    return done('compiler-rt-elf', 'config')


def compiler_rt_elf_built():
    return done('compiler-rt-elf', 'build')


def compiler_rt_elf_installed():
    return done('compiler-rt-elf', 'install')




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


def runtimes_elf_configured():
    return done('runtimes-elf', 'config')


def runtimes_elf_built():
    return done('runtimes-elf', 'build')


def runtimes_elf_installed():
    return done('runtimes-elf', 'install')


def runtimes_musl_configured():
    return done('runtimes-musl', 'config')


def runtimes_musl_built():
    return done('runtimes-musl', 'build')


def runtimes_musl_installed():
    return done('runtimes-musl', 'install')


def qemu_downloaded():
    return done('qemu', 'download')


def qemu_extracted():
    return done('qemu', 'extract')


def qemu_configured():
    return done('qemu', 'config')


def qemu_built():
    return done('qemu', 'build')


def qemu_installed():
    return done('qemu', 'install')


if __name__ == '__main__':
    reset_steps()
