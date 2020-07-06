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
    author='EAVISE, WildMe Developers',
    author_email='dev@wildme.org',
    description='Unified tools for generating PR curves, crunshing image data annotation sets and more',
    long_description=open('README.md').read(),
    # The following settings retreive the version from git.
    # See https://github.com/pypa/setuptools_scm/ for more information
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'write_to': 'brambox/_version.py',
        'write_to_template': '__version__ = "{version}"',
        'tag_regex': '^(?P<prefix>v)?(?P<version>[^\\+]+)(?P<suffix>.*)?$',
        'local_scheme': 'dirty-tag',
    },
    packages=find_packages(),
    scripts=find_scripts(),
    test_suite='tests',
    install_requires=requirements,
)


if __name__ == '__main__':
    setup(**setup_kwargs)
