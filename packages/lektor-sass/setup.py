from setuptools import setup

setup(
    name='lektor-sass',
    version='0.1',
    author=u'Oliver Bestwalter',
    license='MIT',
    py_modules=['lektor_sass'],
    entry_points={'lektor.plugins': ['sass = lektor_sass:SassPlugin']}
)
