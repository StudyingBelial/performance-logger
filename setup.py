from setuptools import setup, find_packages

setup(
    name='sb_perflog',
    vesion='1.0',
    packages=find_packages(),
    install_requires = ['pynvml==12.0.0'],
)