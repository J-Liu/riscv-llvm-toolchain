import requests

from pathlib import Path

from scripts.config import LINUX_TARBALL, NEWLIB_TARBALL, MUSL_TARBALL, \
    TARBALLS_ROOT
from scripts.record_step import store_key, load_key

linux_site = 'https://cdn.kernel.org/pub/linux/kernel/v6.x/'
linux_url = linux_site + LINUX_TARBALL

newlib_site = 'http://sourceware.org/pub/newlib/'
newlib_url = newlib_site + NEWLIB_TARBALL

musl_site = 'https://musl.libc.org/releases/'
musl_url = musl_site + MUSL_TARBALL


def download_tarball(url, name):
    print('Downloading ' + url + ' ...')
    target = Path(TARBALLS_ROOT).joinpath(name)
    if target.exists():
        print(name + ' is already downloaded')
        return
    r = requests.get(url)
    with open(target, 'wb') as f:
        f.write(r.content)
    print(name + ' is downloaded')


def download_tarballs():
    if not load_key('linux-headers', 'download'):
        download_tarball(linux_url, LINUX_TARBALL)
        store_key('linux-headers', 'download', True)
    if not load_key('newlib', 'download'):
        download_tarball(newlib_url, NEWLIB_TARBALL)
        store_key('newlib', 'download', True)
    if not load_key('musl', 'download'):
        download_tarball(musl_url, MUSL_TARBALL)
        store_key('musl-headers', 'download', True)
        store_key('musl', 'download', True)


if __name__ == '__main__':
    download_tarballs()
