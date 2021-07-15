gpip - The Python Package Installer for GitHub
==============================================

gpip is a package installer for Python. You can use gpip to install packages from GitHub repositories.

## Usage: gpip

As default **gpip** uses SSH as git clone default method. You can use a HTTPS GitHub token for clone
private repositories.

```python
from gpip import get

if __name__ == '__main__':
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
```

## Command Line

Use gpip as CLI script to get the packages in a development environment. Inspired in Go get module.

```bash
gpip -g github.com/pomaretta/gpip --https --token your-token --upgrade --force --debug
```