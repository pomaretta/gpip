# ========================= #
# PACKAGER TEST             #
# ========================= #

import os, sys

sys.path.append('{}/../src/private_pip/'.format(os.path.abspath(os.path.dirname(__file__))))
from downloader import clone_repo
from builder import build_package, install_package, clean_dir

if __name__ == "__main__":

    repository = "example-package"
    account = "pomaretta"
    token = ""

    python_instance = "/home/pomaretta/dev/projects/private-pip/env/bin/python3"
    pip3_instance = "/home/pomaretta/dev/projects/private-pip/env/bin/pip3"

    # CLONE REPOSITORY IN TMP
    created, path = clone_repo(repository=repository,github_account=account,token=token,https=True)

    if not created:
        print("Repo not created.")
        exit(-1)

    # BUILD REPOSITORY IN TMP
    build_file = build_package(path=path,instance=python_instance)

    # INSTALL TO LOCAL PIP3 INSTANCE
    installed = install_package(path=path + os.sep + "dist",name=build_file,instance=pip3_instance)

    # Clean installation
    removed = clean_dir(path)

    if removed:
        print("Cannot remove directory.")
        exit(-1)