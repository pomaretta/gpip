#!/usr/bin/env python3

# ========================= #
# BUILDER MODULE            #
# ========================= #

import os
from .exceptions import BuildException, ParameterException

class Builder:
    """
    A builder represents a single instance of the build stage, with a given path will
    execute the "python3 setup.py bdist_wheel" command and this will generate a wheel 
    file that will be returned to the manager. This will return the path and name of the package
    wheel file.
    """

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

        os_options = ('> NUL 2> NUL','> /dev/null 2>&1')[os.name != 'nt']
        executable = ('python','python3')[os.name != 'nt']
        command = f"{executable} setup.py bdist_wheel {os_options}"
        
        if debug:
            command = f"{executable} setup.py bdist_wheel"
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