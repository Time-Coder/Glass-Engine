import wget
import hashlib
import os

def md5(file_name):
    if not os.path.isfile(file_name):
        return ""

    md5_hash = hashlib.md5()
    content = open(file_name, "rb").read()
    md5_hash.update(content)

    return md5_hash.hexdigest()

def download(url, target_file, md5_str):
    target_folder = os.path.dirname(os.path.abspath(target_file))
    if not os.path.isdir(target_folder):
        os.makedirs(target_folder)

    while md5(target_file) != md5_str:
        wget.download(url, target_file)
