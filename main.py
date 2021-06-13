import os
import shutil
import subprocess
import distutils.dir_util
import zipfile

def download():
    links = [
        ("minecraft_server.jar", "https://launcher.mojang.com/v1/objects/f9ae3f651319151ce99a0bfad6b34fa16eb6775f/server.jar"),
        ("minecraft.jar", "https://launcher.mojang.com/v1/objects/465378c9dc2f779ae1d6e8046ebc46fb53a57968/client.jar"),
        ("jinput.jar", "https://libraries.minecraft.net/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar"),
        ("lwjgl.jar", "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl/2.9.1/lwjgl-2.9.1.jar"),
        ("lwjgl_util.jar", "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.1/lwjgl_util-2.9.1.jar"),
        ("jinput.zip", "https://libraries.minecraft.net/net/java/jinput/jinput-platform/2.0.5/jinput-platform-2.0.5-natives-windows.jar"),
        ("lwjgl.zip", "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.1/lwjgl-platform-2.9.1-natives-windows.jar")
    ]
    os.mkdir("downloads")
    os.chdir("downloads")
    for link in links:
        print(link)
        subprocess.run(["curl", link[1], "--output", link[0] ])
    os.chdir("..")


# setup mcp jars folder
def vanilla_jars():
    os.mkdir("mcp")
    os.chdir("mcp")
    shutil.copyfile("../files/mcp751.zip", "mcp751.zip")
    shutil.unpack_archive("mcp751.zip")
    os.remove("mcp751.zip")
    os.chdir("jars")
    shutil.copyfile("../../downloads/minecraft_server.jar", "minecraft_server.jar")
    shutil.copytree("../../files/resources", "resources")
    os.mkdir("bin")
    os.chdir("bin")
    shutil.copyfile("../../../downloads/minecraft.jar", "minecraft.jar")
    shutil.copyfile("../../../downloads/jinput.jar", "jinput.jar")
    shutil.copyfile("../../../downloads/lwjgl.jar", "lwjgl.jar")
    shutil.copyfile("../../../downloads/lwjgl_util.jar", "lwjgl_util.jar")
    os.mkdir("natives")
    os.chdir("natives")
    shutil.copyfile("../../../../downloads/jinput.zip", "jinput.zip")
    shutil.unpack_archive("jinput.zip")
    os.remove("jinput.zip")
    shutil.copyfile("../../../../downloads/lwjgl.zip", "lwjgl.zip")
    shutil.unpack_archive("lwjgl.zip")
    os.remove("lwjgl.zip")
    os.chdir("../../../..")


# install btw into vanilla jars
def btw_jars():
    os.chdir("mcp/jars")
    os.mkdir("temp")
    os.chdir("temp")
    shutil.copyfile("../../../files/BTWMod4-B0000003.zip", "btw.zip")
    shutil.unpack_archive("btw.zip")
    
    os.mkdir("client")
    os.chdir("client")
    shutil.copyfile("../../bin/minecraft.jar", "minecraftjar.zip")
    shutil.unpack_archive("minecraftjar.zip")
    
    # files can't be named aux.class in Windows
    with zipfile.ZipFile("minecraftjar.zip") as minecraftjar:
        with open("../auxclass.txt", "wb") as auxclass:
            auxclass.write(minecraftjar.read("aux.class"))
    
    os.remove("minecraftjar.zip")
    distutils.dir_util.copy_tree("../MINECRAFT-JAR", ".")
    os.chdir("..")
    shutil.make_archive("minecraftjar", "zip", "client")
    
    with zipfile.ZipFile("minecraftjar.zip", "a") as minecraftjar:
        minecraftjar.write("auxclass.txt", "aux.class")
    
    os.rename("minecraftjar.zip", "minecraft.jar")
    
    os.mkdir("server")
    os.chdir("server")
    shutil.copyfile("../../minecraft_server.jar", "minecraftjar.zip")
    shutil.unpack_archive("minecraftjar.zip")
    os.remove("minecraftjar.zip")
    distutils.dir_util.copy_tree("../MINECRAFT_SERVER-JAR", ".")
    os.chdir("..")
    shutil.make_archive("minecraftjar", "zip", "server")
    os.rename("minecraftjar.zip", "minecraft_server.jar")
    
    os.chdir("..")
    os.remove("minecraft_server.jar")
    os.remove("bin/minecraft.jar")
    shutil.copyfile("temp/minecraft.jar", "bin/minecraft.jar")
    shutil.copyfile("temp/minecraft_server.jar", "minecraft_server.jar")
    shutil.rmtree("temp")
    os.chdir("../..")
    

def setup_new_git_repo():
    os.chdir("mcp/src")
    subprocess.run(["git", "init", "."])
    subprocess.run(["git", "add", "minecraft"])
    subprocess.run(["git", "add", "minecraft_server"])
    os.mkdir("resources")
    subprocess.run(["git", "add", "resources"])
    subprocess.run(["git", "commit", "-m\"initial decompile\""])
    subprocess.run(["git", "branch",  "decompile"])
    os.chdir("../..")


def patch():
    os.chdir("mcp/src")
    subprocess.run(["git", "apply", "../../files/btw_decomp_fixes.patch"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m\"fix btw decompile errors\""])
    os.chdir("../..")


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



#download()
vanilla_jars()
btw_jars()
decompile()
setup_new_git_repo()
patch()
#clone_ce()
recompile()
