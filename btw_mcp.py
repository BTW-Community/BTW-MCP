import os
import shutil
import subprocess
import distutils.dir_util
import zipfile
import hashlib
import json
import util

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
	
    with open("runtime/commands.py", "r") as f:
        lines = f.readlines()
    
    lines[705] = lines[705][0:-1] + "\"\"\"\n"
    lines[723] = lines[723][0:-1] + "\"\"\"\n"
    
    with open("runtime/commands.py", "w") as f:
        f.writelines(lines)
	
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
    
# get splashes file from BTW
def btw_splashes():
    os.chdir("mcp")
    with zipfile.ZipFile("../files/BTWMod4-B0000003.zip", "r") as btw:
        if "title" not in os.listdir("src/resources"):
            os.mkdir("src/resources/title")
        with open("src/resources/title/splashes.txt", "wb") as lang:
            lang.write(btw.read("MINECRAFT-JAR/title/splashes.txt"))
    os.chdir("src")
    subprocess.run(["git", "add", "resources"])
    subprocess.run(["git", "commit", "-m\"btw splashes\""])
    os.chdir("../..")


def setup_new_git_repo():
    os.chdir("mcp/src")
    subprocess.run(["git", "init", "."])
    subprocess.run(["git", "add", "minecraft"])
    subprocess.run(["git", "add", "minecraft_server"])
    os.mkdir("resources")
    subprocess.run(["git", "add", "resources"])
    subprocess.run(["git", "commit", "-m\"initial decompile\""])
    subprocess.run(["git", "tag",  "decompile"])
    os.chdir("../..")


def patch():
    os.chdir("mcp/src")
    subprocess.run(["git", "apply", "../../files/btw_decomp_fixes.patch"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m\"fix btw decompile errors\""])
    subprocess.run(["git", "tag", "decomp_fix"])
    os.chdir("../..")


def decompile():
    util.use_openjdk()
    os.chdir("mcp")
    subprocess.run(["runtime/bin/python/python_mcp", "runtime/decompile.py"])
    os.chdir("..")


# clone a git repository at a URL and set it as the src folder
def clone_src(url):
    os.chdir("mcp")
    shutil.rmtree("src")
    subprocess.run(["git", "clone", url])
    os.rename(url.split("/")[-1].split(".")[0], "src")
    os.chdir("..")


def recompile():
    util.use_openjdk()
    os.chdir("mcp")
    if "bin" in os.listdir():
        shutil.rmtree("bin")
    
    subprocess.run(["runtime/bin/python/python_mcp", "runtime/recompile.py"])
    
    if "resources" in os.listdir("src"):
        distutils.dir_util._path_created = {}       # https://stackoverflow.com/a/28055993
        distutils.dir_util.copy_tree("src/resources", "bin/minecraft")
        if "bin" in os.listdir("src/resources"):
            distutils.dir_util.copy_tree("src/resources/lang", "bin/minecraft_server")
    
    os.chdir("..")


def package_release(base, release, directory="release"):
    os.chdir("mcp/src")
    subprocess.run(["git", "checkout", base])
    os.chdir("..")
    
    os.chdir("..")
    recompile()
    os.chdir("mcp")
    
    subprocess.run(["runtime/bin/python/python_mcp", "runtime/updatemd5.py", "--force"])
    os.chdir("src")
    subprocess.run(["git", "checkout", release])
    
    resource_paths = subprocess.run(["git", "diff", base + ":resources", release + ":resources", "--name-only"], capture_output=True, text=True).stdout.split("\n")
    modified_paths = subprocess.run(["git", "diff", base, release, "--name-only", "--diff-filter=M"], capture_output=True, text=True).stdout.split("\n")
    added_paths = subprocess.run(["git", "diff", base, release, "--name-only", "--diff-filter=A"], capture_output=True, text=True).stdout.split("\n")
    paths = modified_paths + added_paths
    
    modified_source_paths = [path for path in modified_paths if path.split("/")[0] == "minecraft" or path.split("/")[0] == "minecraft_server"]
    
    paths_to_patch = [path for path in modified_source_paths if "FC" not in path.split("/")[-1]]
    with open("src.patch", "w") as patch_file:
        patch_file.write(subprocess.run(["git", "diff", base, release] + paths_to_patch, capture_output=True, text=True).stdout)
    
    
    source_paths_to_copy = [path for path in modified_source_paths if "FC" in path] + [path for path in added_paths if path.split("/")[0] == "minecraft" or path.split("/")[0] == "minecraft_server"]
    
    os.chdir("..")
    os.chdir("..")
    recompile()
    os.chdir("mcp")
    subprocess.run(["runtime/bin/python/python_mcp", "runtime/reobfuscate.py"])
    
    
    os.chdir("..")
    os.mkdir(directory)
    os.chdir(directory)
    os.mkdir("client")
    distutils.dir_util.copy_tree("../mcp/reobf/minecraft", "client")
    os.mkdir("server")
    distutils.dir_util.copy_tree("../mcp/reobf/minecraft_server", "server")
    os.mkdir("src")
    os.mkdir("src/resources")
    
    os.chdir("../mcp/src/resources")
    util.copy_list(resource_paths[0:-1], "../../../" + directory + "/src/resources")
    distutils.dir_util.copy_tree("../../../" + directory + "/src/resources", "../../../" + directory + "/client")
    if "lang" in os.listdir("../../../" + directory + "/client"):
        distutils.dir_util.copy_tree("../../../" + directory + "/client/lang", "../../../" + directory + "/server/lang")
    
    os.chdir("..")
    util.copy_list(source_paths_to_copy, "../../" + directory + "/src")
    shutil.copyfile("src.patch", "../../" + directory + "/src/src.patch")
    
    os.chdir("../../" + directory)
    shutil.make_archive("client", "zip", "client")
    shutil.make_archive("server", "zip", "server")
    shutil.rmtree("client")
    shutil.rmtree("server")
    os.chdir("..")
    

def import_release(tag_name = None):
    os.chdir("mcp/src")
    distutils.dir_util.copy_tree("../../release/src", ".")
    subprocess.run(["git", "apply", "src.patch"])
    os.remove("src.patch")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m\"imported release\""])
    if tag_name != None:
        subprocess.run(["git", "tag", tag_name])
    os.chdir("../..")