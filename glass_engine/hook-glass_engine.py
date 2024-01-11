from PyInstaller.utils.hooks import collect_data_files
import os

datas  = collect_data_files('glsl', excludes=["__glcache__*"])
datas += collect_data_files('images', excludes=["__glcache__*"])
datas.append((os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../LICENSE").replace("\\", "/"), 'LICENSE'))
