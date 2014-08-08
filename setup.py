# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='oceanoptics',
    version='0.2.7',
    author='Andreas Poehlmann, Jose A. Jimenez-Berni, Ben Gamari, Simon Dickreuter, Ian Ross Williams',
    author_email='mail@andreaspoehlmann.de',
    packages=['oceanoptics', 'oceanoptics.spectrometers'],
    description='A Python driver for Ocean Optics spectrometers.',
    long_description=open('README.md').read(),
    requires=['python (>= 2.7)', 'pyusb (>= 1.0)', 'numpy'],
)
