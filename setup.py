from setuptools import setup

setup(
    name='obestwalter.github.io',
    author='Oliver Bestwalter',
    url='https://github.com/obestwalter/obestwalter.github.io',
    version='19.11dev1',
    packages=['lebut'],
    install_requires=["python-slugify", "nbformat", "nbconvert"],
    entry_points={'console_scripts': ['lebut = lebut.cli:main']},
)
