import os

def clear_compilation(folder_name):
    for home, dirs, files in os.walk(folder_name):
        for filename in files:
            if filename.endswith(".c"):
                print("remove", home + "/" + filename)
                os.remove(home + "/" + filename)

clear_compilation("glass")
clear_compilation("glass_engine")
