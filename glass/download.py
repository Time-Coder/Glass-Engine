import wget
import hashlib
import os
import time
import requests
from geolite2 import geolite2
import sys
import subprocess
from .GlassConfig import GlassConfig

def md5(file_name):
    if not os.path.isfile(file_name):
        return ""

    md5_hash = hashlib.md5()
    content = open(file_name, "rb").read()
    md5_hash.update(content)

    return md5_hash.hexdigest()

def download(url, target_file, md5_str:str=""):
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

def public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        return response.json().get('origin')
    except:
        return "127.0.0.1"

def is_China_ip(ip_address):
    if ip_address == "127.0.0.1":
        return True

    reader = geolite2.reader()
    location = reader.get(ip_address)
    country = location.get('country', {}).get('iso_code') if location else None
    return country == 'CN'

def is_China_user():
    return is_China_ip(public_ip())

def pip_install(package_name:str):
    if "/" not in package_name:
        install_cmd = [sys.executable, "-m", "pip", "install", package_name]
        if is_China_user():
            install_cmd = [sys.executable, "-m", "pip", "install", package_name, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
        
        return_code = subprocess.call(install_cmd)
        if return_code != 0:
            raise RuntimeError(f"failed to install {package_name}")
    else:
        target_file = GlassConfig.cache_folder + "/" + os.path.basename(package_name)
        download(package_name, target_file)
        install_cmd = [sys.executable, "-m", "pip", "install", target_file]
        return_code = subprocess.call(install_cmd)
        if return_code != 0:
            raise RuntimeError(f"failed to install {package_name}")