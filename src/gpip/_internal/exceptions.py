#!/usr/bin/env python3

# ========================= #
# EXCEPTIONS                #
# ========================= #

class ParameterException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PackageException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CloneException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InstallException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BuildException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)