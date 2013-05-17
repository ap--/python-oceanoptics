# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='OceanOptics',
    version='0.1.0',
    author='Andreas Poehlmann, Jose A. Jimenez-Berni',
    author_email='mail@andreaspoehlmann.de',
    packages=['OceanOptics'],
    url='http://pypi.python.org/pypi/OceanOptics/',
    license='LICENSE.txt',
    description='A Python driver for Ocean Optics spectrometers.',
    long_description=open('README.md').read(),
    install_requires=[
        "python >= 2.7",
        "pyusb >= 1.0",
    ],
)