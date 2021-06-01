import os
import shutil
import subprocess
import distutils.dir_util


def download():
    links = [
    "https://launcher.mojang.com/v1/objects/f9ae3f651319151ce99a0bfad6b34fa16eb6775f/server.jar",
    "https://launcher.mojang.com/v1/objects/465378c9dc2f779ae1d6e8046ebc46fb53a57968/client.jar",
    "https://libraries.minecraft.net/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar",
    "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.1/lwjgl-2.9.1.jar",
    "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.1/lwjgl_util-2.9.1.jar",
    "https://libraries.minecraft.net/net/java/jinput/jinput-platform/2.0.5/jinput-platform-2.0.5-natives-windows.jar",
    "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.1/lwjgl-platform-2.9.1-natives-windows.jar"
    ]
    os.mkdir("downloads")
    os.chdir("downloads")
    for link in links:
        print(link)
        subprocess.run(["curl", link, "--output", link.split("/")[-1] ])
    os.chdir("..")

# setup mcp jars folder

def mcp_jars():
    os.mkdir("mcp")
    os.chdir("mcp")
    shutil.copyfile("../files/mcp751.zip", "mcp751.zip")
    shutil.unpack_archive("mcp751.zip")
    os.remove("mcp751.zip")
    os.chdir("jars")
    shutil.copyfile("../../downloads/server.jar", "minecraft_server.jar")
    shutil.copytree("../../files/resources", "resources")
    os.mkdir("bin")
    os.chdir("bin")
    shutil.copyfile("../../../downloads/client.jar", "minecraft.jar")
    shutil.copyfile("../../../downloads/jinput-2.0.5.jar", "jinput.jar")
    shutil.copyfile("../../../downloads/lwjgl-2.9.1.jar", "lwjgl.jar")
    shutil.copyfile("../../../downloads/lwjgl_util-2.9.1.jar", "lwjgl_util.jar")
    os.mkdir("natives")
    os.chdir("natives")
    shutil.copyfile("../../../../downloads/jinput-platform-2.0.5-natives-windows.jar", "jinput.zip")
    shutil.unpack_archive("jinput.zip")
    os.remove("jinput.zip")
    shutil.copyfile("../../../../downloads/lwjgl-platform-2.9.1-natives-windows.jar", "lwjgl.zip")
    shutil.unpack_archive("lwjgl.zip")
    os.remove("lwjgl.zip")
    os.chdir("../../../..")


def decompile():
    os.chdir("mcp")
    subprocess.run(["runtime/bin/python/python_mcp", "runtime/decompile.py"])
    os.chdir("..")

def clone_ce():
    os.chdir("mcp")
    shutil.rmtree("src")
    subprocess.run(["git", "clone", "https://github.com/BTW-Community/BTW-source.git"])
    os.rename("BTW-source", "src")
    distutils.dir_util.copy_tree("src/resources", "bin/minecraft")
    os.chdir("..")

def recompile():
    os.chdir("mcp")
    subprocess.run(["runtime/bin/python/python_mcp", "runtime/recompile.py"])
    os.chdir("..")


download()
mcp_jars()
decompile()
clone_ce()
recompile()
