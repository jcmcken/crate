from distutils.core import setup

setup(
    name='crate',
    version=open('VERSION').read().strip(),
    description='Manage virtual file repositories with ease',
    author='Jon McKenzie',
    url='http://github.com/jcmcken/crate',
    packages=['crate', 'crate.filters', 'crate.managers'],
    scripts=['bin/crate'],
)
