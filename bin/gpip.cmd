@echo OFF
REM="""
setlocal
set PythonExe=""
set PythonExeFlags=

for %%i in (cmd bat exe) do (
    for %%j in (python.%%i) do (
        call :SetPythonExe "%%~$PATH:j"
    )
)
for /f "tokens=2 delims==" %%i in ('assoc .py') do (
    for /f "tokens=2 delims==" %%j in ('ftype %%i') do (
        for /f "tokens=1" %%k in ("%%j") do (
            call :SetPythonExe %%k
        )
    )
)
%PythonExe% -x %PythonExeFlags% "%~f0" %*
exit /B %ERRORLEVEL%
goto :EOF

:SetPythonExe
if not ["%~1"]==[""] (
    if [%PythonExe%]==[""] (
        set PythonExe="%~1"
    )
)
goto :EOF
"""

# ===================================================
# Python script starts here
# ===================================================

from argparse import ArgumentParser
from gpip import get, __version__
from typing import Tuple

import os
import re

# ========================= #
# GET COMMAND               #
# ========================= #

def get_command(*args,**kwargs):
    get(
        *args,
        **kwargs
    )

# ========================= #
# INSTALL COMMAND           #
# ========================= #

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

def install_command(*args,**kwargs):
    
    if len(args) > 1:
        print("Cannot install more than one file.")
        exit(1)

    # Read file and get gpip packages and pip packages
    pip_packages, gpip_packages = read_file(args[0])

    if len(pip_packages) == 0 and len(gpip_packages) == 0:
        print("Empty file.")
        exit(1)

    # If pip packages install before gpip.
    options = ('> NUL 2> NUL','> /dev/null 2>&1')[os.name != "nt"]
    if len(pip_packages) > 0:
        os.system(f"pip3 install {' '.join(pip_packages)} {(options,'')[kwargs['debug']]}")

    if len(gpip_packages) > 0:
        get_command(
            *gpip_packages
            ,**kwargs
        )

# ========================= #
# VERSION COMMAND           #
# ========================= #

def version_command(*args,**kwargs):
    print("Currently installed version: {}".format(__version__))
    exit(0)

if __name__ == "__main__":

    COMMANDS = {
        "get": get_command,
        "install": install_command,
        "version": version_command,
    }

    parser = ArgumentParser()
    
    # ========================= #
    # NEW #
    # ========================= #

    parser.add_argument(
        'action'
        ,choices=COMMANDS.keys()
        ,help="the action to invoke with %(prog)s"
    )

    parser.add_argument(
        'arguments'
        ,nargs="*"
    )

    parser.add_argument(
        '--debug'
        ,required=False
        ,action="store_true"
        ,help="Enable debug mode."
    )

    get_group = parser.add_argument_group('GET')

    get_group.add_argument(
        '--https'
        ,required=False
        ,action="store_true"
        ,help="Enable HTTPS Mode."
    )

    get_group.add_argument(
        '--token'
        ,required=False
        ,type=str
        ,help="Provide token for https."
    )

    get_group.add_argument(
        '--upgrade'
        ,required=False
        ,action="store_true"
        ,help="Upgrade package."
    )

    get_group.add_argument(
        '--force'
        ,required=False
        ,action="store_true"
        ,help="Force install."
    )

    args = parser.parse_args()
    
    COMMANDS[args.action](
        *args.arguments
        ,https=args.https
        ,token=args.token
        ,upgrade=args.upgrade
        ,force=args.force
        ,debug=args.debug
    )