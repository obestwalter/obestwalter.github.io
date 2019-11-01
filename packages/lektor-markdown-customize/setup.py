from setuptools import setup

name = "lektor-markdown-customize"
module = name.replace("-", "_")

setup(
    name=name,
    version="0.1",
    author="Oliver Bestwalter",
    license="MIT",
    py_modules=[module],
    entry_points={
        "lektor.plugins": [
            f"{name.partition('-')[-1]} = {module}:MarkdownCustomizePlugin"
        ]
    },
)
