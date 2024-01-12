import os

def get_hook_dirs():
    return [os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")]