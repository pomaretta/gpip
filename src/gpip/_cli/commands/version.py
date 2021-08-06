# ========================= #
# VERSION COMMAND           #
# ========================= #

__command__ = "version"

from argparse import ArgumentParser
from typing import Optional, List
from gpip import __version__

def main(
    argv: Optional[List[str]] = None
    ,pwd: str = None
    ,**kwargs
) -> bool:
    print("Currently installed version: {}".format(__version__))
    return True
