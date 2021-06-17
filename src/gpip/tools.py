# ========================= #
# TOOLS MODULE              #
# ========================= #

import importlib.util as imp
import sys, os
import re

from .initializer import GithubPip, Repository, Account, Instance
from .exceptions import PackageError, CloneException, InstallException, BuildException, InstanceException, CleanException

def _checkIfExists(package: str) -> bool:
    # Repositories must name as the packages.
    if package in sys.modules:
        return True
    elif (spec := imp.find_spec(package)) is not None:
        return True
    else:
        return False

def _discoverPackages(packages: list, https: bool = False ,pip: str = None, verbose: bool = False, upgrade: bool = False, force: bool = False) -> list:

    repositories = list()

    for idx, package in enumerate(packages):

        package: str

        account: str
        repository: str

        # Packages must match https path without protocol.
        # github.com/pomaretta/example-package
        pattern = re.compile("(.+@)*([\w\d\.]+)(:[\d]+){0,1}/*")
        search = pattern.match(package)
        if not search:
            raise PackageError(f"Error importing package={package}")

        # Get the owner of the repository.
        account = package.split('/')[1]

        # Get the basename of the repository url.
        repository = os.path.basename(package)

        # Avoid extension .git
        repository = repository.split('.')[0]
        
        if not _checkIfExists(repository) or upgrade or force:
            repositories.append(
                Repository(
                    name=repository
                    ,account=Account(
                        name=account
                        ,https=https
                    )
                    ,pip=GithubPip(
                        account=Account(
                            name=account
                            ,https=https
                        ),
                        instances={
                            "pip": Instance(
                                name="pip"
                                ,path=pip
                            )
                        }
                    )
                    ,upgrade=upgrade
                    ,force=force
                )
            )

    return repositories

def _installPackages(packages: list,verbose: bool = False):

    for package in packages:

        package: Repository

        try:
            package.install()
        except CloneException as cloneException:
            if verbose:
                print(f"Clone error. Package={package.name}. STACK: {str(cloneException)}")
            continue
        except InstanceException as instanceException:
            if verbose:
                print(f"Panic: Instance path error, using ENV instances on {package.name}")
            continue
        except BuildException as buildException:
            if verbose:
                print(f"Fatal: Cannot build repository {package.name} with URL {package.getURL()}")
            break
        except InstallException as installException:
            if verbose:
                print(f"Fatal: Cannot install repository {package.name} with URL {package.getURL()}")
            break
        except CleanException as cleanException:
            if verbose:
                print(f"Clean warning. Package={package.name} STACK: {str(cleanException)}")
            continue

def get(*args, **kwargs):

    https = False
    pip_instance = None
    verbose = False
    upgrade = False
    force = False

    if "https" in kwargs:
        https = kwargs["https"]

    if "pip" in kwargs:
        pip_instance = kwargs["pip"]

    if "verbose" in kwargs:
        verbose = kwargs["verbose"]

    if "upgrade" in kwargs:
        upgrade = kwargs["upgrade"]

    if "force" in kwargs:
        force = kwargs["force"]

    repositories = _discoverPackages(
        args
        ,https=https
        ,pip=pip_instance
        ,verbose=verbose
        ,upgrade=upgrade
        ,force=force
    )

    _installPackages(repositories,verbose=verbose)