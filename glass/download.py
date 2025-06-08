import wget
import hashlib
import os
import time
import requests
import sys
import subprocess


def md5(file_name:str)->str:
    if not os.path.isfile(file_name):
        return ""

    md5_hash = hashlib.md5()
    content = open(file_name, "rb").read()
    md5_hash.update(content)

    return md5_hash.hexdigest()


def download(url, target_file:str, md5_str: str = "")->None:
    target_folder = os.path.dirname(os.path.abspath(target_file))
    if not os.path.isdir(target_folder):
        os.makedirs(target_folder)

    if md5_str:
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

        if md5_str:
            current_md5 = md5(target_file)
            if current_md5 == md5_str:
                return
        else:
            if os.path.isfile(target_file):
                return

        time.sleep(1)

        times += 1
        if times > 4:
            raise RuntimeError(f"download {url} to {target_file} retry over times")
        else:
            print("download failed, retry...")


def pip_raw_install(*args)->None:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *args])
    except:
        import pip
        if hasattr(pip, 'main'):
            pip.main(['install', *args])
        else:
            from pip._internal.cli.main import main as pip_main
            pip_main(['install', *args])


def public_ip()->str:
    try:
        response = requests.get("https://httpbin.org/ip")
        return response.json().get("origin")
    except:
        return "127.0.0.1"


def is_China_ip(ip_address)->bool:
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json/")
        data = response.json()
        return data['country'] == 'CN'
    except Exception as e:
        return True


_is_China_user = None
def is_China_user()->bool:
    global _is_China_user
    if _is_China_user is None:
        _is_China_user = is_China_ip(public_ip())

    return _is_China_user


def pip_install(package: str):
    if is_China_user():
        pip_raw_install(package, "-i", "https://mirrors.aliyun.com/pypi/simple", "--no-warn-script-location")
    else:
        pip_raw_install(package, "--no-warn-script-location")
