# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='oceanoptics',
    version='0.3.2',
    author='Andreas Poehlmann, Jose A. Jimenez-Berni, Ben Gamari, Simon Dickreuter, Ian Ross Williams',
    author_email='mail@andreaspoehlmann.de',
    packages=['oceanoptics', 'oceanoptics.spectrometers'],
    description='Community-coded Python module for oceanoptics spectrometers. This software is not associated with Ocean Optics. Use it at your own risk.',
    long_description=open('README.md').read(),
    requires=['python (>= 2.7)', 'pyusb (>= 1.0)', 'numpy'],
)
