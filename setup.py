from setuptools import setup

setup(
    name="obestwalter.github.io",
    author="Oliver Bestwalter",
    url="https://github.com/obestwalter/obestwalter.github.io",
    version="19.11dev1",
    packages=["lebut"],
    install_requires=[
        "livereload",
        "black",
        "python-slugify",
        "fire",

        # FIXME should be part of typogrify plugin
        "typogrify",

        # FIXME should be part of notebook plugin
        "jupyter",
        "nbconvert",
        "nbformat",
        # atm editable version from master is installed in toxenv
        # "lektor"
    ],
    extras_require={"test": ["pytest"]},
    entry_points={"console_scripts": ["lebut = lebut.cli:main"]},
)
