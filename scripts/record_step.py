import json

from scripts.config import TOP_PATH

step_path = TOP_PATH.joinpath('step').with_suffix('.json')


def reset_steps():
    clang = {
        'git': False,
        'config': False,
        'build': False,
        'install': False
    }
    linux_headers = {
        'download': False,
        'extract': False,
        'config': False,
        'build': False,
        'install': False
    }
    newlib = {
        'download': False,
        'extract': False,
        'config': False,
        'build': False,
        'install': False
    }
    musl_headers = {
        'download': False,
        'extract': False,
        'config': False,
        'build': False,
        'install': False
    }
    compiler_rt = {
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
        'compiler-rt': compiler_rt,
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


if __name__ == '__main__':
    reset_steps()
