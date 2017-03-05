from setuptools import setup

setup(
    name='lektor-typogrify',
    version='0.1',
    author=u'Oliver Bestwalter',
    license='MIT',
    py_modules=['lektor_typogrify'],
    entry_points={
        'lektor.plugins': ['typogrify = lektor_typogrify:TypogrifyPlugin']}
)
