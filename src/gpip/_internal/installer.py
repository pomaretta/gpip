#!/usr/bin/env python3

# ========================= #
# INSTALLER MODULE          #
# ========================= #

import os
from .exceptions import InstallException, ParameterException

class Installer:
 
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
            
        return path, name, upgrade, force, debug
    
    def __install__(self,path: str, name: str, upgrade: bool, force: bool, debug: bool) -> bool:
        """
        Install the package and return if the operation was successfull.
        """
        
        ORIGINAL_CWD = os.getcwd()
        
        os.chdir(path)

        if debug:
            print(f"Installing from {path} with {name} package with upgrade={upgrade} and force={force}")

        command = f"pip3 install {name} {('','--upgrade')[upgrade]} {('','--force-reinstall')[force]} --quiet > /dev/null 2>&1"

        if debug:
            command = f"pip3 install {name} {('','--upgrade')[upgrade]} {('','--force-reinstall')[force]}"
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
            - debug: bool = False
                - Debug mode.
        """
        path, name, upgrade, force, debug = self.__params__(**kwargs)
        return self.__install__(
            path=path,
            name=name,
            upgrade=upgrade,
            force=force,
            debug=debug
        )