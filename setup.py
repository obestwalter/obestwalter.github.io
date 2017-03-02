from setuptools import setup

setup(
    name='oliver.bestwalter.de',
    version='0.0.1dev1',
    author='Oliver Bestwalter',
    url='http://oliver.bestwalter.de',
    packages=['utils'],
    entry_points={
        'console_scripts': [
            'serve = utils.my_lektor:main',
            'draft = utils.workflow:draft',
            'publish = utils.workflow:publish',
            'deploy = utils.workflow:deploy',
        ]
    },
    classifiers=['Programming Language :: Python :: 3.6'],
    scripts=['transpile']
)
