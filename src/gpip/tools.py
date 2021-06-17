# ========================= #
# TOOLS MODULE              #
# ========================= #

import importlib.util as imp
import sys, os
import re

from initializer import Repository, Account
from exceptions import PackageError, CloneException, InstallException, BuildException, InstanceException, CleanException

def _checkIfExists(package: str) -> bool:
    # Repositories must name as the packages.
    if package in sys.modules:
        return True
    elif (spec := imp.find_spec(package)) is not None:
        return True
    else:
        return False

def _discoverPackages(packages: list, https: bool = False ,pip_instance = None) -> list:

    repositories = list()

    for idx, package in enumerate(packages):

        package: str

        account: str
        repository: str

        # Packages must match https path without protocol.
        # github.com/pomaretta/example-package
        search = re.match(r"^github\.com/[a-zA-Z]+/[a-zA-Z]+$",package)
        if not search:
            raise PackageError(f"Error importing package={package}")

        # Get the owner of the repository.
        account = package.split('/')[1]

        # Get the basename of the repository url.
        repository = os.path.basename(package)

        # Avoid extension .git
        package = package.split('.')[0]

        if not _checkIfExists(package):
            repositories.append(
                Repository(
                    name=package
                    ,account=Account(
                        name=account
                        ,https=https
                    )
                    ,pip=pip_instance
                )
            )

    return repositories

def _installPackages(packages: list):

    for package in packages:

        package: Repository

        try:
            package.install()
        except CloneException as cloneException:
            continue
        except InstanceException as instanceException:
            print(f"Panic: Instance path error, using ENV instances on {package.name}")
            continue
        except BuildException as buildException:
            print(f"Fatal: Cannot build repository {package.name} with URL {package.getURL()}")
            break
        except InstallException as installException:
            print(f"Fatal: Cannot install repository {package.name} with URL {package.getURL()}")
            break
        except CleanException as cleanException:
            continue

def get(*args, **kwargs):

    https = False
    pip_instance = None

    if "https" in kwargs:
        https = kwargs["https"]

    if "pip" in kwargs:
        pip_instance = kwargs["pip"]

    repositories = _discoverPackages(args,https=https,pip_instance=pip_instance)

    _installPackages(repositories)