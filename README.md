<div align="center">
<h1><b>gpip</b></h1>

[gpip](https://www.github.com/pomaretta/gpip) is a package installer utility for python

**Sections:** [Syntax](#syntax) — [Commands](#commands) — [Cases](#cases)

<a href="https://github.com/pomaretta/gpip/actions">
    <img src="https://img.shields.io/github/workflow/status/pomaretta/gpip/GPIP%20Test%20%F0%9F%8C%8E/main" alt="Build status" />
</a>

<a href="https://pypi.org/project/gpip/">
    <img src="https://img.shields.io/pypi/v/gpip.svg" />
</a>

<a href="https://pypi.org/project/gpip/">
    <img src="https://img.shields.io/pypi/dm/gpip" />
</a>

</div>

---

**gpip** is a package installer utility for GitHub public and private repositories, is a way to replace the **copy-paste** problem for individuals or organizations that have code inside repositories but cannot make it public, with **gpip** you can handle a repository with more than one package and have versioning and other capabilities.

```
pip3 install gpip
```

---

## **Syntax**

We have a syntax for specify the packages like Go has. We manage to allow some options inside the same line of specification but with easy and simple use.

```html
github.com/<ACCOUNT>/<REPOSITORY><?PATH-WITH-/>:<NAME-OF-PACKAGE>@<BRANCH> <OPTIONS-KEY-VALUE>
```

- The **account** is the name of the GitHub user.
- The **repository** the name of the repository.
- The **path** the path where the package is in, support subdirectories, with '/'. e.g: **path/to/package**
- The **name of package**, as default gpip will take the name of the repository as the package name, but can be defined with ':' after repository name or with path included. e.g: **repo/path:other-name**
- The **branch** specify if the code has to move to other branch before taking action to enter directories, this can be used to test packages that are not in the main branch, or for structure purposes.
- The **options** are the options that the package can handle like: https, token, upgrade, force. Actions that interacts with **pip** utility and **git**. They are separated by ';' and assign values with '=' character. Will be in the end of the line between a space. e.g: **https=true;force=true**

---

## **Commands**

The commands are the utilities itself, we like to be similary to **pip** commands and **go**.

### **Get**

The get command allow the developer to install a package like you do in **pip**, in a development environment.

As example will be installing this package (gpip) in older version with force, to enable **--force-reinstall** option in **pip** command.

```
gpip get github.com/pomaretta/gpip==0.4 force=true
```

### **Install**

The install command can be used with a **requirements** file, and one thing we like is that only need to be one file and declare **pip** and **gpip** packages inside. Only you need to remember to install those packages with **gpip install**

The command works like **pip** install command.

```
gpip install requirements.txt
```

`The definition of the gpip packages are the same in all commands. Using the syntax reference.`


### **Cases**

Yeah, you read all of that, but you know how to use **gpip** now, the powerfull cases that maybe gpip can save your time. Let me guide you throught the different use cases that gpip has. [Check here](https://github.com/pomaretta/gpip/tree/main/readme/CASES.md)