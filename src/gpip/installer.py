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
            - verbose
        """
        
        path: str
        name: str
        upgrade: bool = False
        force: bool = False
        verbose: bool = False
        
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
            
        if "verbose" in kwargs and isinstance(kwargs["verb"],bool):
            verbose = kwargs["verbose"]
            
        return path, name, upgrade, force, verbose
    
    def __install__(self,path: str, name: str, upgrade: bool, force: bool, verbose: bool) -> bool:
        """
        Install the package and return if the operation was successfull.
        """
        
        ORIGINAL_CWD = os.getcwd()
        
        os.chdir(path)

        # TODO: Debug option

        command = f"pip3 install {name} {('','--upgrade')[upgrade]} {('','--force-reinstall')[force]} --quiet > /dev/null 2>&1"
    
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
            - verbose: bool = False
                - Verbose mode.
            
        """
        path, name, upgrade, force, verbose = self.__params__(**kwargs)
        return self.__install__(
            path=path,
            name=name,
            upgrade=upgrade,
            force=force,
            verbose=verbose,
        )