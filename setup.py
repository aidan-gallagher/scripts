from setuptools import setup

setup(
    name='aidans scripts',
    version='1.0',
    description='Aidans miscellaneous scripts',
    author='Aidan Gallagher',
    install_requires=['fabric', 'git_filter_repo'],
    scripts=[
        'build_and_install/build_and_install.py',
        'git_fixup.py'
    ]
)
