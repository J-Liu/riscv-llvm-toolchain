from scripts.init import init_dir
from scripts.user_input import user_input
from scripts.download import download_tarballs
from scripts.git_clone import clone_code

user_input()
init_dir()
download_tarballs()
clone_code()