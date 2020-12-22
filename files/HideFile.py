import os

def hide_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            rename_file = "." + name
            print(os.path.join(root, rename_file))
            print(os.path.join(root, name))
            return os.rename(os.path.join(root, name), os.path.join(root, rename_file))


print(hide_file("build.xml.txt","/users/deepak.babu/downloads"))