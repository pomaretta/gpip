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
    
    PACKAGE_EXPRESSION = "^(?P<source>github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)(?P<path>(/[A-Za-z0-9_.\-]+)*)(?P<name>(:[A-Za-z0-9_.\-]+)*)(?P<version>(==[A-Za-z0-9_.\-]+)*)(?P<branch>(@[A-Za-z0-9_./\-]+)*)( (?P<options>[A-Za-z0-9_.;=\-]+)?)?$"

    def __init__(self,**kwargs):
        self.kwargs = kwargs
        self.downloader = Downloader()
        self.builder = Builder()
        self.installer = Installer()
        pass

    def __remove_character__(self,string: str,character: str) -> str:
        return string.replace(character,'')

    def __validate_package__(self,package: str) -> bool:
        return re.compile(self.PACKAGE_EXPRESSION).match(package)

    def __package_data__(self,data: str):

        available_params = [
            "https",
            "token",
            "force",
            "upgrade"
        ]

        params = dict()

        for param in available_params:
            params[param] = None

        items = data.split(';')

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

    def __package_source__(self,data: str) -> Tuple[str,str]:
        
        EXPRESSION = "^(?P<source>github\.com)(?P<account>/[A-Za-z0-9_.\-]+)(?P<repository>/[A-Za-z0-9_.\-]+)?$"

        data = re.match(EXPRESSION,data)

        # NOTE: Source of repository (github.com)
        source = data.group('source')

        # NOTE: Account of repository (name)
        account = data.group('account')
        account = self.__remove_character__(account,'/')

        # NOTE: Name of repository (repository)
        repository = data.group('repository')
        repository = self.__remove_character__(repository,'/')

        return repository, account 

    def __source__(self, url: str):
        """
        Parse the package data and return the corresponding parameters.

        - source
            - Package name (Name of repository)
        - account
            - The account of the repository
        - directory
            - Directory to enter if specified
        - branch
            - Branch to checkout if specified
        - version
            - Version to checkout if specified
        - package_name
            - If a package name if specified over source name

        """
        
        # NOTE: Parser packages.

        # github.com/account/package
        # github.com/account/package:package-name==version@branch
        # github.com/account/package:package-name==version@branch force=true;upgrade=true;https=true;token=TOKEN

        # NOTE: Source basic parameters
        source: str
        account: str
        directory: str = None
        branch: str = None
        version: str = None
        self.package_name: str = None

        # NOTE: Override parameters if specified
        repository_https: bool = None
        repository_token: str = None
        repository_force: bool = None
        repository_upgrade: bool = None

        # ========================= #
        # NEW METHOD OF PARSE       #
        # ========================= #

        repository = re.match(
            self.PACKAGE_EXPRESSION,
            string=url
        )

        # NOTE: Get the source (repository name + account)
        source, account = self.__package_source__(repository.group('source'))

        # NOTE: Get the path of directory if specified, need to be normalized '/\' with os.sep
        directory = repository.group('path')

        if directory != None:
            directory = directory.replace('\\',os.sep).replace('/',os.sep).replace('\\','',1).replace('/','',1)

        # NOTE: Get package name if specified, normalize ':'
        self.package_name = repository.group('name')

        if self.package_name != None:
            self.package_name = self.__remove_character__(self.package_name,':')
    
        # NOTE: Get version if specified, normalize '=='
        version = repository.group('version')
    
        if version != None:
            version = self.__remove_character__(version,'==')

        # NOTE: Get branch if specified, normalize '@'
        branch = repository.group('branch')

        if branch != None:
            branch = self.__remove_character__(branch,'@')
    
        # NOTE: Parse options, trim first space.
        options = repository.group('options')

        if options != None:
            options = options.strip() # Remove spaces.
            repository_https, repository_token, repository_force, repository_upgrade = self.__package_data__(options)

        if source == "" and isinstance(account,str):
            source = None
            
        if directory == "" and isinstance(account,str):
            directory = None

        if account == "" and isinstance(account,str):
            account = None

        if branch == "" and isinstance(branch,str):
            branch = None

        if version == "" and isinstance(version,str):
            version = None

        if self.package_name == "" and isinstance(self.package_name,str):
            self.package_name = None

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

        if not self.__validate_package__(url):
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
        
        os_options = ("> NUL 2> NUL","> /dev/null 2>&1")[os.name != "nt"]
        command = "pip3 show {} {}"

        if os.system(command.format(source,os_options)) == 0:
            return True

        if self.package_name != None and os.system(command.format(self.package_name,os_options)) == 0:
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
            print(f"Installing {(source,self.package_name)[self.package_name != None]} from {account}")

        return self.installer.install(
            path=package_path
            ,name=package_name
            ,force=force
            ,upgrade=upgrade
            ,debug=debug
        ) 
