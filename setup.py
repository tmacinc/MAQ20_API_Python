from distutils.core import setup

from setuptools import find_packages

setup(
    name="maq20",
    version="0.10.0",
    packages=find_packages(),
    url="https://github.com/DataforthCorporation/MAQ20_API_Python",
    license="LICENSE.txt",
    author="Dataforth Corporation",
    author_email="techinfo@dataforth.com",
    description="Python modules for Dataforth MAQ20 Data Acquisition System",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
