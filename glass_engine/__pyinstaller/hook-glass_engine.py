from PyInstaller.utils.hooks import collect_data_files
import os

datas  = collect_data_files('glsl', excludes=['__glcache__'])
datas.append((os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/images/glass_engine_logo64.png", "images"))
datas.append((os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../../LICENSE").replace("\\", "/"), ""))