#!/usr/bin/env python3

# ========================= #
# GPIP SETUP 				#
# ========================= #

import setuptools

# ========================= #
# DESCRIPTION 				#
# ========================= #

with open("README.md", "r") as fh:
    long_description = fh.read()

# ========================= #
# SETUP 					#
# ========================= #

setuptools.setup(
	name='gpip',  
	version='0.1',
	scripts=[
		"src/gpip/bin/gpip"
	]
	,author="Carlos Pomares",
	author_email="cpomaresp@gmail.com",
	description="A PIP Private Utility Package.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/pomaretta/gpip",
	package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
	install_requires= [
		"setuptools"
		,"pip"
		,"wheel"
	]
	,classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	],
)