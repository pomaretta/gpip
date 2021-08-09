# ========================= #
# TOOLS MODULE              #
# ========================= #

from ._internal.repository import Repository

def __discover_repositories__(*args, **kwargs) -> list:
    repositories = list()
    for repository in args:
        repositories.append(
            Repository(
                url=repository,
                **kwargs
            )
        )
    return repositories

def __install_packages__(*args) -> None:
    for repository in args:
        repository.install()

def get(*args, **kwargs):
    """
    Declare packages using gpip syntax from Public and Private repositories
    from GitHub, you can specify many as you want as args and use different
    functionalities passing key-value arguments.

    - args: list
        - Specify the packages with the gpip syntax.
    - kwargs: dict
        - Specify some key-value arguments to enable or use some functionalities.

    Package declaration:

    - Using syntax you can declare a package to get from GitHub.
        - github.com/<ACCOUNT>/<REPOSITORY>
        - github.com/<ACCOUNT>/<REPOSITORY>/<PATH> -- Specify path as you will do in a path.
        - github.com/<ACCOUNT>/<REPOSITORY>==<VERSION> -- Specify a version to use (Git Tag)
        - github.com/<ACCOUNT>/<REPOSITORY>:<NAME> -- Specify an alternative name than the repository one.
        - github.com/<ACCOUNT>/<REPOSITORY>@<BRANCH> -- Specify a branch to checkout.
        - github.com/<ACCOUNT>/<REPOSITORY> <SPACE> <OPTIONS-KEY-VALUE> -- Use some option inside a package declaration.
        - You can use at the same declaration the above syntax.
        - github.com/pomaretta/gpip:gpip==0.4@main force=true

    Optional arguments (kwargs):

    - https: bool = False
        - Specify to use HTTPS as clone method.
    - token: str = None
        - Specify a token to use with HTTPS.
    - force: bool = False
        - Specify to force reinstall package, feature of pip.
    - upgrade: bool = False
        - Specify to upgrade package, feature of pip.
    - debug: bool = False
        - Enable loggin and show some execution information.
    - output: str = None
        - Specify the location to store cloned repositories from GitHub, default using
        temp directory.

    """
    __install_packages__(
        *__discover_repositories__(
            *args
            ,**kwargs
        )
    )