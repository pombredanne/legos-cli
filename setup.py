from setuptools import setup

setup(
    name='legos',
    version='0.1',
    py_modules=['legos_command'],
    install_requires=['Click','PyGithub','arrow', 'tabulate'],
    entry_points='''
        [console_scripts]
        legos=legos_command:cli
    ''',
    )