#!/usr/bin/env python3

# ========================= #
# DOWNLOADER UTIL           #
# ========================= #

import tempfile
import os

from .exceptions import CloneException

class Downloader:
    """
    Performs downloads in case the docker image has to be build from
    GitHub private or public repository.
    """
    def __params__(self,**kwargs):
        """
        Read the kwargs and extracts the desired data from it:
            - source
            - account
            - https
            - output
            - directory
        """

        source: str
        account: str
        token: str = None
        https: bool = False
        output: str = None
        directory: str = None
        
        if "source" in kwargs and isinstance(kwargs["source"],str):
            source = kwargs["source"]

        if "account" in kwargs and isinstance(kwargs["account"],str):
            account = kwargs["account"]

        if "https" in kwargs and isinstance(kwargs["https"],bool):
            https = kwargs["https"]

        if "token" in kwargs and isinstance(kwargs["token"],str):
            token = kwargs["token"]

        if "output" in kwargs and isinstance(kwargs["output"],str):
            output = kwargs["output"]

        if "directory" in kwargs and isinstance(kwargs["directory"],str):
            directory = kwargs["directory"]

        return source, account, https, token, output, directory

    def __clone__(self,source: str, account: str, https: bool, token: str, output: str, directory: str) -> str:
        """
        Clone the given repository and returns the path of the tmp.
        """

        ORIGINAL_CWD = os.getcwd()

        # Get the repository to perform clones.
        tmp_directory = tempfile.mkdtemp(prefix=f"{source + account}")

        if output != None:
            tmp_directory = output

        # Change CWD to tmp directory
        os.chdir(tmp_directory)

        # Establish the clone method. Default ssh
        command = f"git@github.com:{account}/{source}"

        if https:
            command = f"https://www.github.com/{account}/{source}"
        
        if https and token != None:
            command = f"https://{token}@github.com/{account}/{source}"
        
        # Form the clone command
        clone_command = "git clone {} --quiet 2> /dev/null".format(command)

        # Clone the repository
        operation = os.system(clone_command)
        
        if operation != 0:
            raise CloneException(f"cannot clone the repository")

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
        
        """
        # TODO: Add verbose and dry mode.
        source, account, https, token, output, directory = self.__params__(**kwargs)
        return self.__clone__(
            source=source,
            account=account,
            https=https, 
            token=token,
            output=output,
            directory=directory
        )