# ========================= #
# BUILDER MODULE            #
# ========================= #

import os
import sys
import shutil

def build_package(path: str, instance: str = None) -> str:

    executor = "python3"

    if instance != None:
        executor = instance

    original_cwd = os.getcwd()

    # CHANGE CWD TO PATH
    os.chdir(path)

    # EXECUTE PACKAGE
    os.system(f"{executor} setup.py bdist_wheel")

    # DISCOVER PACKAGE NAME
    os.chdir(path + os.sep + "dist")
    
    package = os.listdir(".")[0]

    os.chdir(original_cwd)

    return package

def install_package(path: str, name: str, instance: str = None) -> bool:

    executor = "pip3"

    if instance != None:
        executor = instance

    original_cwd = os.getcwd()

    # CHANGE CWD TO PATH
    os.chdir(path)

    os.system(f"{executor} install ./{name}")

    os.chdir(original_cwd)

    return name in sys.modules

def clean_dir(path: str) -> bool:
    shutil.rmtree(path)
    return os.path.exists(path)
