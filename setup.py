import setuptools as setup
from pkg_resources import get_distribution, DistributionNotFound


def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None

def find_packages():
    return ['brambox'] + ['brambox.'+p for p in setup.find_packages('brambox')]


def find_scripts():
    return setup.findall('scripts')


def get_version():
    with open('VERSION', 'r') as f:
        version = f.read().splitlines()[0]
    with open('brambox/version.py', 'w') as f:
        f.write('#\n')
        f.write('# Brambox version: Automatically generated version file\n')
        f.write('# Copyright EAVISE\n')
        f.write('#\n\n')
        f.write(f'__version__ = "{version}"\n')

    return version


requirements = [
    'pyyaml',
    'numpy',
    'scipy',
    'matplotlib',
]
pillow_req = 'pillow-simd' if get_dist('pillow-simd') is not None else 'pillow'
requirements.append(pillow_req)

setup.setup(
    name='brambox',
    version=get_version(),
    author='EAVISE',
    description='Unified tools for generating PR curves, crunshing image data annotation sets and more',
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts=find_scripts(),
    test_suite='tests',
    install_requires=requirements,
)
