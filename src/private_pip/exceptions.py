# ========================= #
# EXCEPTIONS                #
# ========================= #

class CloneException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InstanceException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InstallException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BuildException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CleanException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)