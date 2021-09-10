from setuptools import setup

setup(
    name='aidans scripts',
    version='1.0',
    description='Aidans miscellaneous scripts',
    author='Aidan Gallagher',
    install_requires=['fabric'],
    scripts=[
        'build_and_install/build_and_install.py'
    ]
)
