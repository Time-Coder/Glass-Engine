import wget
import hashlib
import os
import time
import requests

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

    current_md5 = md5(target_file)
    if current_md5 == md5_str:
        return

    times = 0
    while True:
        if os.path.isfile(target_file):
            os.remove(target_file)

        print(f"downloading {os.path.basename(target_file)}...")
        try:
            wget.download(url, target_file)
        except:
            respond = requests.get(url)
            if respond.status_code != 200:
                raise RuntimeError(respond.content)
            
            out_file = open(target_file, "wb")
            out_file.write(respond.content)
            out_file.close()

        current_md5 = md5(target_file)
        if current_md5 == md5_str:
            return

        time.sleep(1)

        times += 1
        if times > 20:
            raise RuntimeError(f"download {url} to {target_file} retry over times")
        else:
            print("download failed, retry...")
