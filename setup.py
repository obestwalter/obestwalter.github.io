from setuptools import setup

setup(
    name='oliver.bestwalter.de',
    version='0.0.1dev1',
    author='Oliver Bestwalter',
    url='http://oliver.bestwalter.de',
    packages=['utils'],
    entry_points={
      'console_scripts': [
          'draft = utils.workflow:draft',
          'publish = utils.workflow:publish',
      ]
    },
)
