===================================
gpip - Package Installer for GitHub
===================================

.. image:: https://img.shields.io/github/workflow/status/pomaretta/gpip/GPIP%20Test%20%F0%9F%8C%8E/main
.. image:: https://img.shields.io/pypi/v/gpip.svg
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
.. image:: https://img.shields.io/pypi/dm/gpip

**gpip** is a package installer utility for GitHub public and private repositories, is a way to replace the **copy-paste** problem for individuals or organizations that have code inside repositories but cannot make it public, with **gpip** you can handle a repository with more than one package and have versioning and other capabilities.

Features
--------

* Install packages from private or public repositories
* Allow to use versioning, branch and path location from repositories
* Easy and powerfull syntax to declare packages.
* Command Line interface similar to **pip** and **go**

Quickstart
----------

Install the latest version of gpip in your global **pip** repository or **virtualenv** if you haven't installed it yet.

.. code-block:: bash

    pip3 install gpip

Install your private/public packages directly from **GitHub**

.. code-block:: bash

    gpip get github.com/username/repository/path:package-name

You can place the same package syntax inside a requirements file and place both **pip** and **gpip** packages inside.

.. code-block:: bash

    gpip install requirements.txt

Syntax
------

We have a syntax for specify the packages like Go has. We manage to allow some options inside the same line of specification but with easy and simple use.

.. code-block:: python

    "github.com/<ACCOUNT>/<REPOSITORY>" # Simple
    "github.com/<ACCOUNT>/<REPOSITORY>:<PACKAGE-NAME>" # Different name than repository
    "github.com/<ACCOUNT>/<REPOSITORY>==<VERSION>" # Get a specified version with Git Tags
    "github.com/<ACCOUNT>/<REPOSITORY>/path/to/package" # If package is inside subdirectories
    "github.com/<ACCOUNT>/<REPOSITORY>@<BRANCH>" # If the package is on other branch
    "github.com/<ACCOUNT>/<REPOSITORY> force=true;https=true" # If you like to declare options in the package declaration
    "github.com/<ACCOUNT>/<REPOSITORY>/path/to/package:<PACKAGE-NAME>" # You can use the different options in the same declaration.

* The **account** is the name of the GitHub user.
* The **repository** the name of the repository.
* The **path** the path where the package is in, support subdirectories, with '/'. e.g: **path/to/package**
* The **name of package**, as default gpip will take the name of the repository as the package name, but can be defined with ':' after repository name or with path included. e.g: **repo/path:other-name**
* The **version**, you can specify a version to checkout, uses Git Tags for work.
* The **branch** specify if the code has to move to other branch before taking action to enter directories, this can be used to test packages that are not in the main branch, or for structure purposes.
* The **options** are the options that the package can handle like: https, token, upgrade, force. Actions that interacts with **pip** utility and **git**. They are separated by ';' and assign values with '=' character. Will be in the end of the line between a space. e.g: **https=true;force=true**

Examples
--------

**GET**

As example will be installing this package (gpip) in older version with force, to enable **--force-reinstall** option in **pip** command.

.. code-block:: bash

    # With force declared inside package declaration.
    gpip get "github.com/pomaretta/gpip==0.4 force=true"

    # With force from CLI parameter.
    gpip get github.com/pomaretta/gpip==0.4 --force

**INSTALL**

The install command can be used with a **requirements** file, and one thing we like is that only need to be one file and declare **pip** and **gpip** packages inside. Only you need to remember to install those packages with **gpip install**

.. code-block:: bash

    gpip install requirements.txt

**PROGRAMMATICALLY**

You can use the **get** command inside your scripts.

.. code-block:: python

    from gpip import get

    get(
        "github.com/<ACCOUNT>/<REPOSITORY>" # Simple
        ,"github.com/<ACCOUNT>/<REPOSITORY>:<PACKAGE-NAME>" # Different name than repository
        ,"github.com/<ACCOUNT>/<REPOSITORY>==<VERSION>" # Get a specified version with Git Tags
        ,"github.com/<ACCOUNT>/<REPOSITORY>/path/to/package" # If package is inside subdirectories
        ,"github.com/<ACCOUNT>/<REPOSITORY>@<BRANCH>" # If the package is on other branch
        ,"github.com/<ACCOUNT>/<REPOSITORY> force=true;https=true" # If you like to declare options in the package declaration
        ,force=True | False # Force option, default False
        ,debug= True | False # Debug option, shows commands and other information
        ,https= True | False # Https option, Default False
        ,token="your-token" # With HTTPS, use a GitHub token to clone repositories
        ,upgrade= True | False # Upgrade option, from pip
    )

    # After get command from gpip you are ready to use your recently installed packages.

    from recently_installed_package import things


Command Line Interface
----------------------

The following are some of the sub-commands you may find:

.. code-block:: bash
    
    Commands:
      GET       Get packages from GitHub repository.
      INSTALL   Get packages from Pip and GitHub repositories, declared in a file.
      VERSION   Show the current installed version of gpip.

Cases
-----

Yeah, you read all of that, but you know how to use **gpip** now, the powerfull cases that maybe gpip can save your time. Let me guide you through the different use cases that gpip has.
`Check here`_.

.. _`Check here`: https://github.com/pomaretta/gpip/tree/main/readme/CASES.md