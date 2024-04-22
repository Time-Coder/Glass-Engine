import os

self_folder = os.path.dirname(os.path.abspath(__file__))
datas = [
    (os.path.abspath(self_folder + "/../LICENSE").replace("\\", "/"), "assimpy"),
    (os.path.abspath(self_folder + "/assimp/LICENSE").replace("\\", "/"), "assimpy/assimp"),
    (os.path.abspath(self_folder + "/pybind11/LICENSE").replace("\\", "/"), "assimpy/pybind11")
]
