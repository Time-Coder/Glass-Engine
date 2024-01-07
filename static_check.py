import os

def check_folder(folder_name):
    for home, dirs, files in os.walk(folder_name):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                os.system("pyflakes " + home + "/" + filename)

check_folder("glass")
check_folder("glass_engine")
