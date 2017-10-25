from setuptools import setup

setup(
    name='legos',
    version='1.0',
    py_modules=['legos_command'],
    install_requires=['Click','PyGithub','arrow', 'tabulate'],
    entry_points='''
        [console_scripts]
        legos=legos_command:cli
    ''',
    )