#!/usr/bin/env python3

# ========================= #
# BUILDER MODULE            #
# ========================= #

import os
from .exceptions import BuildException, ParameterException

class Builder:
    
    def __params__(self,**kwargs):
        """
        Read the kwargs and extracts the desired data from it:
            - path
            - debug
        """
        
        path: str
        debug: bool = False
        
        if not "path" in kwargs or not isinstance(kwargs["path"],str):
            raise ParameterException("missing path in build request")
        
        path = kwargs["path"]
        
        if "debug" in kwargs and not isinstance(kwargs["debug"],bool):
            debug = kwargs["debug"]
        
        return path, debug
    
    def __build__(self,path: str, debug: bool):
        """
        Build the project and returns the path of the directory and Build Distributed Package (wheel).
        """
        
        ORIGINAL_CWD = os.getcwd()
        
        if debug:
            print(f"Building from {path}")
        
        os.chdir(path)
        
        command = f"python3 setup.py bdist_wheel > /dev/null 2>&1"
        
        if debug:
            command = f"python3 setup.py bdist_wheel"
            print("Running with {}".format(command))
        
        operation = os.system(command)
        
        if operation != 0:
            raise BuildException("cannot perform build")

        dist = os.listdir(os.path.join(path,'dist'))[0]
        
        os.chdir(ORIGINAL_CWD)
        
        return os.path.join(path,'dist'), dist
    
    def build(self,**kwargs):
        """
        Build the package of the given directory and returns the directory and package name installer, if an error occurs raises
        a BuildException.
            - path: str
                - Source path where the repository stands.
            - debug: bool = False
                - Enable debug mode.
        """
        path, debug = self.__params__(**kwargs)
        return self.__build__(
            path=path,
            debug=debug
        )