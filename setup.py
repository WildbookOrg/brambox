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


def parse_version(fpath):
    """
    Statically parse the version number from a python file

    """
    import ast
    from os.path import exists

    if not exists(fpath):
        raise ValueError('fpath={!r} does not exist'.format(fpath))
    with open(fpath, 'r') as file_:
        sourcecode = file_.read()
    pt = ast.parse(sourcecode)

    class VersionVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if getattr(target, 'id', None) == '__version__':
                    self.version = node.value.s

    visitor = VersionVisitor()
    visitor.visit(pt)
    return visitor.version



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
    version=parse_version('brambox/__init__.py'),
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
