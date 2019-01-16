#!/usr/bin/env python
# coding: UTF-8

from setuptools import find_packages, setup

setup(
        name='linux_aio',
        version='0.1.0',
        packages=find_packages(),
        provides=['linux_aio'],
        platforms='Linux',
        setup_requires=['cffi>=1.0.0'],
        cffi_modules=['linux_aio/raw/syscall.py:ffibuilder'],
        install_requires=['cffi>=1.0.0'],
)
