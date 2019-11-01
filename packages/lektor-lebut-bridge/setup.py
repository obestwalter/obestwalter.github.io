from setuptools import setup

name = "lektor-lebut-bridge"
module = name.replace("-", "_")

setup(
    name=name,
    description="Do site specific things as part of lektor build/dev.",
    version="0.1.dev1",
    author="Oliver Bestwalter",
    author_email="oliver@bestwalter.de",
    url=(
        "https://github.com/obestwalter/obestwalter.github.io/tree/lektor-sources/"
        f"packages/{name}"
    ),
    py_modules=[module],
    entry_points={
        "lektor.plugins": [
            f"{name.partition('-')[-1]} = {module}:LebutPlugin"
        ]
    },
    install_requires=["nbformat", "nbconvert"],
)
