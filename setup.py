#!/usr/bin/env python
# coding: UTF-8

from setuptools import find_packages, setup

with open('README.md') as fp:
    readme = fp.read()

setup(
        name='linux_aio',
        version='0.2.1',
        author='Byeonghoon Yoo',
        author_email='bh322yoo@gmail.com',
        description='Linux aio ABI wrapper',
        long_description=readme,
        long_description_content_type='text/markdown',
        url='https://github.com/isac322/linux_aio',
        packages=find_packages(),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: C',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System',
            'Topic :: System :: Filesystems',
            'Topic :: System :: Operating System',
            'Topic :: System :: Operating System Kernels',
            'Topic :: System :: Operating System Kernels :: Linux',
        ],
        license='LGPLv3+',
        keywords='Linux AIO ABI API wrapper',
        python_requires='>=3.4',
        provides=['linux_aio'],
        platforms='Linux',
        setup_requires=['cffi>=1.0.0'],
        install_requires=['cffi>=1.0.0'],
        cffi_modules=['linux_aio/raw/syscall.py:_ffibuilder'],
        package_data={
            'linux_aio': ['py.typed'],
            'linux_aio.raw': ['*.pyi'],
        }
)
