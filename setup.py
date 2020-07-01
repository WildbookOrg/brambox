# -*- coding: utf-8 -*-
from setuptools import findall, find_packages, setup
from pkg_resources import get_distribution, DistributionNotFound


def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None

def find_scripts():
    return findall('scripts')


def get_version():
    with open('VERSION', 'r') as f:
        version = f.read().splitlines()[0]
    with open('brambox/version.py', 'w') as f:
        f.write('#\n')
        f.write('# Brambox version: Automatically generated version file\n')
        f.write('# Copyright EAVISE\n')
        f.write('#\n\n')
        f.write('__version__ = "{}"\n'.format(version))

    return version


requirements = [
    'pyyaml',
    'numpy',
    'scipy',
    'matplotlib',
]
pillow_req = 'pillow-simd' if get_dist('pillow-simd') is not None else 'pillow'
requirements.append(pillow_req)


setup_kwargs = dict(
    name='wbia-brambox',
    version=get_version(),
    author='EAVISE, WildMe Developers',
    author_email='dev@wildme.org',
    description='Unified tools for generating PR curves, crunshing image data annotation sets and more',
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts=find_scripts(),
    test_suite='tests',
    install_requires=requirements,
)


if __name__ == '__main__':
    setup(**setup_kwargs)
