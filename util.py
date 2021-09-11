import os
import shutil

def copy_list(paths, destination):
    for path in paths:
        dirs = path.split("/")
        p = destination + "/"
        for dir in dirs[0:-1]:
            if dir not in os.listdir(p):
                os.mkdir(p + dir + "/")
            p += dir + "/"
        shutil.copyfile(path, p + dirs[-1])


def use_openjdk():
    os.environ["PATH"] = os.getcwd() + "\\files\\jdk8u302-b08\\bin;" + os.environ["PATH"]