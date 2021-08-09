# ========================= #
# GPIP SETUP 				#
# ========================= #

import os

from setuptools import setup, find_packages

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()

def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

# ========================= #
# SETUP 					#
# ========================= #

long_description = read('README.rst')

setup(
	name="gpip",
	version=get_version("src/gpip/__init__.py"),
	description="Utility tool for installing Python packages from GitHub repositories.",
	long_description=long_description,
	license="MIT",
	url="https://github.com/pomaretta/gpip",
	author="Carlos Pomares",
	author_email="cpomaresp@gmail.com",
	package_dir={"": "src"},
	packages=find_packages(
		where="src",
		exclude=["test","scripts"],
	),
	scripts=[
		"bin/gpip",
		"bin/gpip.cmd"
	],
	classifiers=[
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Topic :: Software Development :: Build Tools",
		'Topic :: Software Development',
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		'Operating System :: OS Independent',
	],
	install_requires=[
		"setuptools"
		,"pip"
		,"wheel"
	],
	python_requires=">=3.6",
)