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
from typing import Tuple

class Repository:
    
    def __init__(self,**kwargs):
        self.kwargs = kwargs
        self.downloader = Downloader()
        self.builder = Builder()
        self.installer = Installer()
        pass

    def __validate_url__(self,url: str) -> bool:
        return re.compile("(.+@)*([\w\d\.]+)(:[\d]+){0,1}/*").match(url)

    def __package_data__(self,data: str) -> Tuple[str,str,str]:

        available_params = [
            "name",
            "branch",
            "version",
            "https",
            "token",
            "force",
            "upgrade"
        ]

        params = dict()

        for param in available_params:
            params[param] = None

        # available_params = {
        #     "name": None
        #     ,"branch": None
        #     ,"version": None
        # }

        items = data.split(';')

        # if len(items) == 0:
        #     return available_params["name"], available_params["branch"], available_params["version"]

        if len(items) == 0:

            d = list()

            for name, value in params.items():
                d.append(value)

            return tuple(d)

        for item in items:
            values = item.split('=')

            if len(values) == 0:
                raise ParameterException("invalid value")

            identifier = values[0]
            value = values[1]

            if identifier.lower() not in available_params:
                raise ParameterException("unkown parameter")

            params[identifier] = value

        d = list()

        for name, value in params.items():
            d.append(value)

        return tuple(d)

    def __source__(self, url: str):
        
        # Parse url
        # github.com/pomaretta/gpip
        # github.com/pomaretta/gpip@directory

        source: str
        account: str
        directory: str = None
        branch: str = None
        version: str = None
        self.package_name: str = None

        repository_https: bool = None
        repository_token: str = None
        repository_force: bool = None
        repository_upgrade: bool = None

        repository = os.path.basename(url)

        # Get the source, example: gpip (Repository name)
        if re.search(r"[a-zA-Z0-9-._]+[^@#]",repository) != None:
            source = re.search(r"[a-zA-Z0-9-._]+[^@#]",repository).group(0)
        
        # Get the directory if exists.
        if re.search(r"@[a-zA-Z0-9-._]+[^#]",repository) != None:
            directory = re.search(r"@[a-zA-Z0-9-._]+[^#]",repository).group(0).replace('@','')
        
        # Get the package name if specified.
        if re.search(r"#[a-zA-Z0-9-._;]+[^@]",repository) != None:
            self.package_name, branch, version, repository_https, repository_token, repository_force, repository_upgrade = self.__package_data__(re.search(r"#[a-zA-Z0-9-._=;]+[^@]",repository).group(0).replace('#',''))
        
        # Get account
        account = re.search(r"/[a-zA-Z0-9]+/", url).group(0).replace('/','')

        if source == "" and isinstance(account,str):
            source = None
            
        if directory == "" and isinstance(account,str):
            directory = None

        if account == "" and isinstance(account,str):
            account = None

        return source, account, directory, branch, version, repository_https, repository_token, repository_force, repository_upgrade

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

        repository_https: bool = None
        repository_token: str = None
        repository_force: bool = None
        repository_upgrade: bool = None

        source \
        ,account \
        ,directory \
        ,branch \
        ,version \
        ,repository_https \
        ,repository_token \
        ,repository_force \
        ,repository_upgrade = self.__source__(url)
        
        if repository_https != None:
            https = repository_https.lower() == "true"

        if repository_token != None and isinstance(repository_token,str):
            token = repository_token

        if repository_force != None:
            force = repository_force.lower() == "true"
        
        if repository_upgrade != None:
            upgrade = repository_upgrade.lower() == "true"

        return source, account, directory, branch, version, https, token, output, upgrade, force, debug

    def __exists__(self) -> bool:
        
        source \
        ,account \
        ,directory \
        ,branch \
        ,version \
        ,https \
        ,token \
        ,output \
        ,upgrade \
        ,force \
        ,debug = self.__parse__(**self.kwargs)
        
        command = "pip3 show {} > /dev/null 2>&1"

        if os.system(command.format(source)) == 0:
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
        ,branch \
        ,version \
        ,https \
        ,token \
        ,output \
        ,upgrade \
        ,force \
        ,debug = self.__parse__(**self.kwargs)
       
        if self.__exists__() and not force:
            return True
        
        install_path = self.downloader.download(
            source=source
            ,account=account
            ,directory=directory
            ,branch=branch
            ,version=version
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
            print(f"Installing {source} from {account}")

        return self.installer.install(
            path=package_path
            ,name=package_name
            ,force=force
            ,upgrade=upgrade
            ,debug=debug
        ) 
