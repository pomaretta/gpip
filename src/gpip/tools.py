# ========================= #
# TOOLS MODULE              #
# ========================= #

from .repository import Repository

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
    __install_packages__(
        *__discover_repositories__(
            *args
            ,**kwargs
        )
    )