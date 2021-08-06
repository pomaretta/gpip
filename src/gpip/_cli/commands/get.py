# ========================= #
# GET COMMAND               #
# ========================= #

__command__ = "get"

from argparse import ArgumentParser
from typing import Optional, List
from gpip import get

def main(
    argv: Optional[List[str]] = None
    ,pwd: str = None
    ,**kwargs
) -> bool:
    
    parser = ArgumentParser(
        prog="Get Command"
        ,description="Install packages from gpip url."
        ,add_help=True
    )

    parser.add_argument(
        'packages'
        ,nargs="*"
        ,type=str
        ,help="The packages to install."
    )

    args = parser.parse_args(argv or ())

    if len(args.packages) == 0:
        parser.print_help()
        exit(1)

    get(
        *args.packages,
        **kwargs
    )

    return True