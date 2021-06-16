import setuptools

# Description
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name='privatepip',  
	version='0.1',
	author="Carlos Pomares",
	author_email="carlos.pomares@webbeds.com",
	description="A PIP Private Utility Package.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/pomaretta/private-pip",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)