#!/usr/bin/env python3

# ========================= #
# REPOSITORY MODULE         #
# ========================= #

import re
import os

from .downloader import Downloader
from .builder import Builder
from .installer import Installer
from .exceptions import ParameterException, PackageException

class Repository:
    
    def __init__(self,**kwargs):
        self.kwargs = kwargs
        self.downloader = Downloader()
        self.builder = Builder()
        self.installer = Installer()
        pass

    def __validate_url__(self,url: str) -> bool:
        return re.compile("(.+@)*([\w\d\.]+)(:[\d]+){0,1}/*").match(url)

    def __source__(self, url: str):
        
        # Parse url
        # github.com/pomaretta/gpip
        # github.com/pomaretta/gpip@directory

        source: str
        account: str
        directory: str = None
        self.package_name: str = None

        repository = os.path.basename(url)

        # Get source
        # source = re.search(r"[a-zA-Z0-9-.]+[^@]",repository).group(0)
        
        # # Get directory if exists
        # if len(repository.split("@")) > 1:
        #     directory = repository.split("@")[1]
        
        # TODO: Package, Directory, Name
        if re.search(r"[a-zA-Z0-9-._]+[^@#]",repository) != None:
            source = re.search(r"[a-zA-Z0-9-._]+[^@#]",repository).group(0)
        
        if re.search(r"@[a-zA-Z0-9-._]+[^#]",repository) != None:
            directory = re.search(r"@[a-zA-Z0-9-._]+[^#]",repository).group(0).replace('@','')
        
        if re.search(r"#[a-zA-Z0-9-._]+[^@]",repository) != None:
            self.package_name = re.search(r"#[a-zA-Z0-9-._]+[^@]",repository).group(0).replace('#','')
        
        # Get account
        account = re.search(r"/[a-zA-Z0-9]+/", url).group(0).replace('/','')

        if source == "" and isinstance(account,str):
            source = None
            
        if directory == "" and isinstance(account,str):
            directory = None

        if account == "" and isinstance(account,str):
            account = None

        return source, account, directory

    def __parse__(self,**kwargs):
        
        url: str
        https: bool = False
        token: str = None
        output: str = None
        upgrade: bool = None
        force: bool = None
        debug: bool = False
        
        # ========================= #
        # REQUIRED PARAMETERS       #
        # ========================= #

        if not "url" in kwargs and not isinstance(kwargs["url"], str):
            raise ParameterException("missing url parameter")

        url = kwargs["url"]

        if not self.__validate_url__(url):
            raise PackageException("invalid package url")

        # ========================= #
        
        if "https" in kwargs and isinstance(kwargs["https"],bool):
            https = kwargs["https"]
            
        if "token" in kwargs and isinstance(kwargs["token"],str):
            token = kwargs["token"]
            
        if "output" in kwargs and isinstance(kwargs["output"],str):
            output = kwargs["output"]
            
        if "upgrade" in kwargs and isinstance(kwargs["upgrade"],bool):
            upgrade = kwargs["upgrade"]
            
        if "force" in kwargs and isinstance(kwargs["force"],bool):
            force = kwargs["force"]
            
        if "debug" in kwargs and isinstance(kwargs["debug"],bool):
            debug = kwargs["debug"]

        source \
        ,account \
        ,directory = self.__source__(url)
        
        return source, account, directory, https, token, output, upgrade, force, debug

    def __exists__(self) -> bool:
        
        source \
        ,account \
        ,directory \
        ,https \
        ,token \
        ,output \
        ,upgrade \
        ,force \
        ,debug = self.__parse__(**self.kwargs)
        
        characters = [
            "-"
            ,"_"
            ,"."
        ]

        command = "pip3 show {} > /dev/null 2>&1"

        for char in characters:
            c = re.sub(f"[-_.]",f"{char}",source)
            # c = source.replace(r"-|_|.",char)
            if debug:
                print("Performing existence test of {}".format(c))
            if os.system(command.format(c)) == 0:
                return True
            
        if self.package_name != None and os.system(command.format(self.package_name)) == 0:
            return True

        return False

    def install(self):
        """
        Install the repository package.
        """
        
        source \
        ,account \
        ,directory \
        ,https \
        ,token \
        ,output \
        ,upgrade \
        ,force \
        ,debug = self.__parse__(**self.kwargs)
        
        install_path = self.downloader.download(
            source=source
            ,account=account
            ,directory=directory
            ,https=https
            ,token=token
            ,output=output
            ,debug=debug
        )
        
        package_path, package_name = self.builder.build(
            path=install_path
            ,debug=debug
        )

        if not self.__exists__() and not debug:
            print(f"Installing {source} from {account} using https={https}{('',f' ({token})')[token != None]}")

        # Install
        if force or not self.__exists__():
            return self.installer.install(
                path=package_path
                ,name=package_name
                ,force=force
                ,upgrade=upgrade
                ,debug=debug
            )
        
        return True