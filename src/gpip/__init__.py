"""
gpip is a package installer that can be used to install packages from
GitHub repositories, this allow the user to manage a private repository and
place there all the packages that are available there. This allows to manage a lot of packages
from individuals or organization that cannot be made public. And have a way to organise code and avoid
copy-pasting through repositories.
"""

__version__ = "0.4.3"

from .tools import get
