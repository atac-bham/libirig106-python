#!/usr/bin/env python

"""Initialize submodule and do install. Also adds clean command."""

from distutils.cmd import Command
from glob import glob
from shutil import rmtree
import os
import sys

from setuptools import setup, Extension


class Clean(Command):
    """Cleans build and dist directories."""

    description = 'clean build and dist directories'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_items = ['build', 'dist', 'i106.egg-info', '.cache', '.eggs',
                       '.pytest_cache']
        build_items += glob('*.so')
        for path in build_items:
            if os.path.exists(path):
                if os.path.isdir(path):
                    rmtree(path)
                else:
                    os.remove(path)


# Install base library if missing
try:
    if not os.listdir('src/libirig106'):
        os.system('git submodule init && git submodule update')
except Exception as err:
    print(err)


# Define flags based on platform.
if sys.platform == 'win32':
    FLAGS = ['/Od', '/EHsc', '/MT']
    LINK_FLAGS = []
else:
    FLAGS = [
        '-c',
        '-std=c99',
        '-fPIC',
        '-Wall',
        '-D_FILE_OFFSET_BITS=64',
        '-D_LARGEFILE64_SOURCE',
        '-ggdb',
    ]
    LINK_FLAGS = ['-fPIC']

EXT = Extension(
    'i106',
    glob('src/*.c') + glob('src/libirig106/src/*.c'),
    depends=glob('src/*.h') + glob('src/libirig106/src/*.h'),
    extra_compile_args=FLAGS,
    extra_link_args=LINK_FLAGS,
)

setup(
    name='i106',
    version='0.0.1',
    ext_modules=[EXT],
    cmdclass={'clean': Clean},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
