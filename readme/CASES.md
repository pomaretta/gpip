# **Use cases of gpip**

## **Cases**

`1. One repository, bunch of packages and different versions.`

gpip can handle subdirectories, branch and version with Git repositories the requirement is to know about Git and GitHub, the versioning works with Git Tags.

You have two packages with each one a version. One needs to be forced because in your local environment is already installed in a newer version.

Using get command throught CLI.

```
gpip get github.com/your-account/repository/dir/package1:my-key-package --force
```

In that case you have specified a package that is inside a subdirectory and the package name dont match with repository name. 

`You must specify the package name if dont match with the repository one, using the ':' character after the repository name or path.`

If you can install multiple packages in the same line and each one have their options you can use the option modifier

```
gpip get "github.com/your-account/repository/dir/package1:my-key-package force=true" github.com/your-account/repository/dir/package2:my-other-package
```

`Using options you will need to encapsulate with ""`