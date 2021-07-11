# ========================= #
# INITIALIZER MODULE        #
# ========================= #

import os
from re import U

from .downloader import clone_repo
from .builder import build_package, install_package, clean_dir
from .exceptions import *

class Account:
    def __init__(self,name: str, token: str = None, https: bool = False) -> None:
        self.name = name
        self.token = token
        self.https = https

class Repository:
    def __init__(self,name: str,directory: str = None,account: Account = None, pip = None, upgrade: bool = None, force: bool = None) -> None:
        self.name = name
        self.directory = directory
        self.account = account
        self.pip = pip
        self.upgrade = upgrade
        self.force = force
        self.installed = dict()
    def getURL(self):
        return f"{('','https://')[self.account.https]}{('git',self.account.token)[self.account.token != None]}@github.com{(':','/')[self.account.https]}{self.account.name}/{self.name}"
    def install(self):
    
        self.pip: GithubPip

        python_path = "python3"
        pip_path = "pip3"

        # ========================= #
        # CLONE STEP                #
        # ========================= #

        try:
            created, path = clone_repo(
                repository=self.name
                ,github_account=self.account.name
                ,token=self.account.token
                ,https=self.account.https
                ,directory=self.directory
            )
        except Exception as e:
            raise CloneException(str(e))

        if not created:
            raise CloneException("Cannot clone the repository")

        # ========================= #
        # BUILD STEP                #
        # ========================= #

        if self.pip.instances != None and "python" in self.pip.instances and not isinstance(self.pip.instances["python"],Instance):
            raise InstanceException("Cannot find Python path in instances or the instance is not of Instance.")
        
        if self.pip.instances != None and "python" in self.pip.instances:
            python_path = self.pip.instances["python"].path

        try:
            build_file = build_package(path,python_path)
        except Exception as e:
            raise BuildException(str(e))

        # ========================= #
        # INSTALL STEP              #
        # ========================= #

        if self.pip.instances != None and "pip" in self.pip.instances and not isinstance(self.pip.instances["pip"],Instance):
            raise InstanceException("Cannot find Pip path in instances or the instance is not of Instance.")

        if self.pip.instances != None and "pip" in self.pip.instances:
            pip_path = self.pip.instances["pip"].path

        upgrade = False
        force = False

        if self.upgrade != None:
            upgrade = self.upgrade

        if self.force != None:
            force = self.force

        try:
            installed = install_package(
                path=(path + os.sep + "dist")
                ,name=build_file
                ,instance=pip_path
                ,upgrade=upgrade
                ,force=force
            )
        except Exception as e:
            raise InstallException(str(e))

        # ========================= #
        # CLEAN STEP                #
        # ========================= #

        try:
            removed = clean_dir(path=path)
        except Exception as e:
            raise CleanException(str(e))

        if not removed:
            raise CleanException("Cannot clean the directory.")

class Instance:
    def __init__(self,name: str,path: str) -> None:
        self.name = name
        self.path = path

class GithubPip:
    def __init__(self,account: Account,instances: dict = None,output: str = None, verbose: bool = False) -> None:
        self.account = account
        self.instances = instances
        self.output = output
        self.repositories = dict()
        self.errors = list()
        self.fatal = list()
    def importRepositories(self,input_list: list):

        repositories = list()

        for repo in input_list:
            repositories.append(
                Repository(
                    os.path.basename(repo)
                    ,self.account
                    ,self
                )
            )

        self.instanceRepositories(repositories=repositories)

    def instanceRepositories(self, repositories: list):

        for idx, r in enumerate(repositories):
            
            r: Repository

            try:
                r.install()
            except CloneException as cloneException:
                if str(cloneException) == "Cannot clone the repository":
                    self.errors.append(f"Cannot clone {r.name} with {r.getURL()} url.")
                else:
                    self.errors.append(f"Cannot find {r.name} with {r.getURL()} url.")
                continue
            except InstanceException as instanceException:
                print(f"Panic: Instance path error, using ENV instances on {r.name}")
                continue
            except BuildException as buildException:
                print(f"Fatal: Cannot build repository {r.name} with URL {r.getURL()}")
                self.fatal.append(str(buildException))
                break
            except InstallException as installException:
                print(f"Fatal: Cannot install repository {r.name} with URL {r.getURL()}")
                self.fatal.append(str(installException))
                break
            except CleanException as cleanException:
                self.errors.append(f"Cannot remove the tmp files of {r.name}")
                continue

            self.repositories[r.name] = r
