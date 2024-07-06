from setuptools import setup, find_packages

setup(
    name='tuna',
    version='0.1',
    py_modules=['cli'],
    requires=[
        'halo', 
        'inquirer',
        'requests',
        'jupyterlab',
        'nbformat'
    ],
    entry_points={
        'console_scripts': [
            'tuna=tuna.cli.main:main',
        ],
    },
)
