#!/usr/bin/env python3

# ========================= #
# INSTALLER MODULE          #
# ========================= #

import os
from .exceptions import InstallException, ParameterException

class Installer:
    """
    This class is the responsible of the installation of the package, this will accept a given path and name
    of package wheel file and will install it to the environment pip executable.    
    """

    def __params__(self,**kwargs):
        """
        Read the kwargs and extracts the desired data from it:
            - path (directory)
            - name (wheel package)
            - upgrade
            - force
            - debug
        """
        
        path: str
        name: str
        upgrade: bool = False
        force: bool = False
        debug: bool = False
        user: bool = False
        
        if not "path" in kwargs or not isinstance(kwargs["path"],str):
            raise ParameterException("missing path in install request")
        
        if not "name" in kwargs or not isinstance(kwargs["name"],str):
            raise ParameterException("missing name in install request")
        
        path = kwargs["path"]
        name = kwargs["name"]
        
        if "upgrade" in kwargs and isinstance(kwargs["upgrade"],bool):
            upgrade = kwargs["upgrade"]
            
        if "force" in kwargs and isinstance(kwargs["force"],bool):
            force = kwargs["force"]
            
        if "debug" in kwargs and isinstance(kwargs["debug"],bool):
            debug = kwargs["debug"]

        if "user" in kwargs and isinstance(kwargs["user"],bool):
            user = kwargs["user"]
            
        return path, name, upgrade, force, user, debug
    
    def __install__(self,path: str, name: str, upgrade: bool, force: bool, user: bool, debug: bool) -> bool:
        """
        Install the package and return if the operation was successfull.
        """
        
        ORIGINAL_CWD = os.getcwd()
        
        os.chdir(path)

        if debug:
            print(f"Installing from {path} with {name} package with upgrade={upgrade}, force={force} and user={user}")

        os_options = ('> NUL 2> NUL','> /dev/null 2>&1')[os.name != 'nt']
        command = f"pip3 install {name} {('','--upgrade')[upgrade]} {('','--force-reinstall')[force]} {('','--user')[user]} --quiet {os_options}"

        if debug:
            command = f"pip install {name} {('','--upgrade')[upgrade]} {('','--force-reinstall')[force]} {('','--user')[user]}"
            print("Running with command {}".format(command))
    
        operation = os.system(command)
        
        if operation != 0:
            raise InstallException("cannot install package.")
        
        os.chdir(ORIGINAL_CWD)
        
        return True
    
    def install(self,**kwargs) -> bool:
        """
        Install a package and if was successfull returns True if not raises an InstallException.
            - path: str
                - Path of the directory containing the package.
            - name: str
                - The package name (file name of wheel package).
            - upgrade: bool = False
                - Enable upgrade install of pip package.
            - force: bool = False
                - Enable force install of pip package.
            - user: bool = False
                - Use --user flag with pip.
            - debug: bool = False
                - Debug mode.
        """
        path, name, upgrade, force, user, debug = self.__params__(**kwargs)
        return self.__install__(
            path=path,
            name=name,
            upgrade=upgrade,
            force=force,
            user=user,
            debug=debug
        )