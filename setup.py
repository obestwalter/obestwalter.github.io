from setuptools import setup

setup(
    name='oliver.bestwalter.de',
    version='2.0.0dev1',
    author='Oliver Bestwalter',
    url='http://oliver.bestwalter.de',
    packages=['utils'],
    entry_points={'console_scripts': ['ob = utils.cli:main']},
    classifiers=['Programming Language :: Python :: 3.6'],
)
