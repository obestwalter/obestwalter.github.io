from setuptools import setup

setup(
    name='lektor-footnoty',
    version='0.1',
    author=u'Oliver Bestwalter',
    license='MIT',
    py_modules=['lektor_footnoty'],
    entry_points={
        'lektor.plugins': [
            'footnoty = lektor_sass:SassPlugin',
        ]
    }
)
