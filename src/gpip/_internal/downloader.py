#!/usr/bin/env python3

# ========================= #
# DOWNLOADER UTIL           #
# ========================= #

import tempfile
import os

from logging import Logger, getLogger
from .exceptions import CloneException, ParameterException

class Downloader:
    """
    The downloader is the class that has the functionality to download the repository,
    this will download the necesary files and will perform some directory operations.
    Like enter some specified directory or checkout to some branch or version.
    
    Is the responsible for manage the repository using git functionalities.
    """
    def __params__(self,**kwargs):
        """
        Read the kwargs and extracts the desired data from it:
            - source
            - account
            - https
            - output
            - directory
            - debug
        """

        source: str
        account: str
        token: str = None
        https: bool = False
        output: str = None
        directory: str = None
        debug: bool = False

        branch: str = None
        version: str = None
                
        if not "source" in kwargs or not isinstance(kwargs["source"],str):
            raise ParameterException("missing source in clone request")
        
        if not "account" in kwargs or not isinstance(kwargs["account"],str):
            raise ParameterException("missing account in clone request")

        source = kwargs["source"]
        account = kwargs["account"]

        if "https" in kwargs and isinstance(kwargs["https"],bool):
            https = kwargs["https"]

        if "token" in kwargs and isinstance(kwargs["token"],str):
            token = kwargs["token"]

        if "output" in kwargs and isinstance(kwargs["output"],str):
            output = kwargs["output"]

        if "directory" in kwargs and isinstance(kwargs["directory"],str):
            directory = kwargs["directory"]

        if "branch" in kwargs and isinstance(kwargs["branch"],str):
            branch = kwargs["branch"]

        if "version" in kwargs and isinstance(kwargs["version"],str):
            version = kwargs["version"]

        if "debug" in kwargs and isinstance(kwargs["debug"],bool):
            debug = kwargs["debug"]

        return source, account, https, token, output, directory, branch, version, debug

    def __clone__(self,source: str, account: str, https: bool, token: str, output: str, directory: str, branch: str, version: str, debug: bool) -> str:
        """
        Clone the given repository and returns the path of the tmp.
        """

        os_options = ('> NUL 2> NUL','> /dev/null 2>&1')[os.name != 'nt']
        ORIGINAL_CWD = os.getcwd()

        # ========================= #
        # CLONE OUTPUT              #
        # ========================= #

        # Get the repository to perform clones.
        tmp_directory = tempfile.mkdtemp(prefix=f"{source + account}")

        if output != None:
            tmp_directory = output

        # TODO: Show all data from package.
        if debug:
            print(f"Cloning {source} from {account} on output={output}\nUsing https={https} with token={token}\nChange to branch={branch}, version={version}\nEnter into directory={directory}")

        # Change CWD to tmp directory
        os.chdir(tmp_directory)

        # ========================= #
        # CLONE COMMAND             #
        # ========================= #

        # Establish the clone method. Default ssh
        command = f"git@github.com:{account}/{source}"

        if https:
            command = f"https://www.github.com/{account}/{source}"
        
        if https and token != None:
            command = f"https://{token}@github.com/{account}/{source}"
        
        # Form the clone command
        clone_command = "git clone {} --quiet {}".format(command,os_options)

        if debug:
            clone_command = "git clone {}".format(command)
            print("Running command {}".format(command))

        # Clone the repository
        operation = os.system(clone_command)
        
        if operation != 0:
            raise CloneException(f"cannot clone the repository")

        # ========================= #
        # BRANCH AND VERSION        #
        # ========================= #

        os.chdir(os.path.join(tmp_directory,source))

        # Change branch
        branch_change = "git checkout -m {} {}".format(branch,os_options)
        
        if branch != None and os.system(branch_change) != 0:
            raise CloneException(f"cannot change branch")

        # Checkout version if exists
        version_change = "git checkout {} {}".format(version,os_options)

        if version != None and os.system(version_change) != 0:
            raise CloneException(f"cannot change version")

        # NOTE: Issue, trying to enter a directory of a branch or version specified that not exists in main branch.
        # Get into the directory if specified
        if directory != None:
            os.chdir(os.path.join(tmp_directory,source,directory))

        # ========================= #
        # CLEAN EXECUTION           #
        # ========================= #

        # Back to original CWD
        os.chdir(ORIGINAL_CWD)

        if directory != None:
            return os.path.join(tmp_directory,source,directory)
    
        return os.path.join(tmp_directory,source)

    def download(self,**kwargs) -> str:
        """
        Returns the path of the cloned repository. If a directory is given, this will
        be set into the CWD and other data will be deleted.
        For clone the repository the given parameters must be at least:
            - source: str
                - Source repository from take the data.
            - account: str (Default will be the account of the source)
                - Specify the account (Can be a name or a token)
            - https: bool = False (Default uses ssh)
                - If true the repository will be cloned using HTTPS.
            - token: str = None
                - The token to clone with.
            - output: str = None
                - The output where the data will be written.
            - directory: str = None
                - If this option is set, this will return the path of the specified directory,
                    if cannot be accessed will return an exception else will
                    return the path of the directory.
            - branch: str = None
                - The branch to create build.
            - version: str = None
                - The tag checkout.
            - debug: bool = False
                - Enable the debug mode and show messages.
        """
        source, account, https, token, output, directory, branch, version, debug = self.__params__(**kwargs)
        return self.__clone__(
            source=source,
            account=account,
            https=https, 
            token=token,
            output=output,
            directory=directory,
            branch=branch,
            version=version,
            debug=debug
        )