import requests

from pathlib import Path

from conf.conf import LINUX_TARBALL, LINUX_URL, MUSL_TARBALL, MUSL_URL, \
    NEWLIB_TARBALL, NEWLIB_URL, TARBALL_ROOT
from utils.record_step import is_linux_headers_downloaded, \
    is_musl_downloaded, is_newlib_downloaded, linux_headers_downloaded, \
    musl_downloaded, musl_headers_downloaded, newlib_downloaded


def download_tarball(url, name):
    print('Downloading ' + url + ' ...')
    target = Path(TARBALL_ROOT).joinpath(name)
    if target.exists():
        print(name + ' is already downloaded')
        return
    r = requests.get(url)
    with open(target, 'wb') as f:
        f.write(r.content)
    print(name + ' is downloaded')


def download_tarballs():
    if not is_linux_headers_downloaded():
        download_tarball(LINUX_URL, LINUX_TARBALL)
        linux_headers_downloaded()
    if not is_newlib_downloaded():
        download_tarball(NEWLIB_URL, NEWLIB_TARBALL)
        newlib_downloaded()
    if not is_musl_downloaded():
        download_tarball(MUSL_URL, MUSL_TARBALL)
        musl_headers_downloaded()
        musl_downloaded()


if __name__ == '__main__':
    download_tarballs()
