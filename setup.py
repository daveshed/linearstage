from setuptools import setup, find_packages
setup(
    name="linearstage",
    version="0.2.2",
    packages=find_packages(),
    install_requires=['RPi.GPIO'],
)