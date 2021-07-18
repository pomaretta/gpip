gpip - The Python Package Installer for GitHub
==============================================

gpip is a package installer for Python. You can use gpip to install packages from GitHub repositories.

## Usage: gpip

As default **gpip** uses SSH as git clone default method. You can use a HTTPS GitHub token for clone
private repositories.

```python

# Import your public packages and gpip
from ... import ...
from gpip import get

# Add your private packages with their options
get(
    "github.com/pomaretta/gpip"
    ,"github.com/pomaretta/other-package"
    ,https=True|False # Enable HTTPS
    ,token="your-token" # Use token with HTTPS
    ,output="clone-output" # Specify where to clone the repositories
    ,force=True|False # Use --force-reinstall option of pip
    ,upgrade=True|False # Use --upgrade option of pip
    ,debug=True|False # Enable debug mode
)

# More than one call with other options.
get(
    "github.com/pomaretta/other-package"
    ,https=False # May be performed with SSH over HTTPS.
    ,debug=False # You can enable options with each package.
)

# Once the packages are installed you can call the imports.
from recently_package import things

# your code ...
```

## Command Line

Use gpip as CLI script to get the packages in a development environment. Inspired in Go get module.

GET command:

```bash
gpip get github.com/pomaretta/gpip github.com/pomaretta/other-package --https --token your-token --upgrade --force --debug
```

INSTALL command:

```bash
gpip install ./private-requirements.txt --https --token your-token --upgrade --force --debug
```