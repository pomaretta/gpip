# ========================= #
# DOWNLOADER UTIL           #
# ========================= #

import tempfile
import os

# Clone a given repository
def clone_repo(repository: str,github_account: str, token: str = None, output: str = None, https: bool = False):

    if github_account == "":
        raise ValueError("Cannot clone from empty account.")

    output_path = tempfile.gettempdir()
    original_cwd = os.getcwd()

    if output != None:
        output_path = output

    account = "git"

    if token != None:
        account = token

    # CHANGE EXECUTION TO OUTPUT PATH
    os.chdir(output_path)

    command = f"git clone {account}@github.com:{github_account}/{repository}"

    if https:
        command = f"git clone https://{account}@github.com/{github_account}/{repository}"
    
    # GET THE REPO IN LOCAL TMP
    os.system(command)

    # Return to original CWD
    os.chdir(original_cwd)

    # RETURN IF THE GIT CLONE EXISTS
    return os.path.exists(output_path + os.sep + repository), (output_path + os.sep + repository)