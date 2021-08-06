# ========================= #
# INSTALL COMMAND           #
# ========================= #

__command__ = "install"

from typing import Optional, List, Tuple
from argparse import ArgumentParser
from gpip import get

import re
import os

def is_gpip_package(package: str) -> bool:
    expression  = "^(?P<source>github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)(?P<path>(/[A-Za-z0-9_.\-]+)*)(?P<name>(:[A-Za-z0-9_.\-]+)*)(?P<version>(==[A-Za-z0-9_.\-]+)*)(?P<branch>(@[A-Za-z0-9_./\-]+)*)( (?P<options>[A-Za-z0-9_.;=\-]+)?)?$"
    return re.compile(expression).match(package)

def read_file(path: str) -> Tuple[list,list]:

    pip = list()
    gpip = list()

    with open(path,'r') as fp:
        out = fp.readlines()
        fp.close()

    # Read all lines.
    for x in out:
        # Avoid commented lines or empty lines.
        if x.startswith('#') or x == "":
            continue
        if is_gpip_package(x):
            gpip.append(x.replace('\n',''))
        else:
            pip.append(x.replace('\n',''))

    return pip, gpip

def main(
    argv: Optional[List[str]] = None
    ,pwd: str = None
    ,**kwargs
) -> bool:

    parser = ArgumentParser(
        prog="Install command"
        ,description="Install pip and gpip packages from specific file."
        ,add_help=True
    )

    parser.add_argument(
        'file'
        ,nargs=1
        ,type=str
        ,help="Path to file."
    )

    args = parser.parse_args(argv or ())

    if len(args.file) > 1:
        print("Cannot install more than one file.")
        exit(1)

    # Read file and get gpip packages and pip packages
    pip_packages, gpip_packages = read_file(args.file[0])

    if len(pip_packages) == 0 and len(gpip_packages) == 0:
        print("Empty file.")
        exit(1)

    # If pip packages install before gpip.
    options = ('> NUL 2> NUL','> /dev/null 2>&1')[os.name != "nt"]
    if len(pip_packages) > 0:
        os.system(f"pip3 install {' '.join(pip_packages)} {(options,'')[kwargs['debug']]}")

    if len(gpip_packages) > 0:
        get(
            *gpip_packages
            ,**kwargs
        )

    return True