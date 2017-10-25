from setuptools import setup

setup(
    name='legos',
    version='1.0',
    description='command line tool to fetch details from github projects/nuget packages',
    author='Prashant Cholachagudda',
    author_email='pvc@outlook.com',
    py_modules=['legos_command'],
    install_requires=['Click','PyGithub','arrow', 'tabulate'],
    entry_points='''
        [console_scripts]
        legos=legos_command:cli
    ''',
    )