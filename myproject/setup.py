from distutils.command.install_scripts import install_scripts
from gettext import install
from importlib.resources import Package
from zipfile import ZIP_STORED
from setuptools import find_packages, setup
from setuptools import find_packages, setup

setup(
    name = 'flaskr',
    version = '1.0.0',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = ['flask',
    ],
)