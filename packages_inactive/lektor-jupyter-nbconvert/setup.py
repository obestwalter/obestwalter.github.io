from setuptools import setup

setup(
    name="lektor-jupyter-nbconvert",
    description="Add preliminary build step to convert .ipynb to .lr",
    version="0.1dev1",
    author="Oliver Bestwalter",
    author_email="oliver@bestwalter.de",
    url=(
        "https://github.com/obestwalter/obestwalter.github.io/tree/lektor-sources/"
        "packages/lektor-jupyter-nbconvert"
    ),
    py_modules=["lektor_jupyter_nbconvert"],
    entry_points={
        "lektor.plugins": [
            "jupyter-nbconvert = lektor_jupyter_nbconvert:JupyterNbConvertPlugin"
        ]
    },
    install_requires=["nbformat", "nbconvert"],
)
