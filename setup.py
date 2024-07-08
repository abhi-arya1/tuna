"""

Pip Setup for Tuna

"""

from setuptools import setup, find_packages

setup(
    name='tuna',
    version='0.1',
    py_modules=['cli'],
    packages=find_packages(),
    install_requires=[
        'inquirer',
        'requests',
        'halo',
        'jupyterlab',
        'nbformat',
        'scikit-learn',
        'tabulate',
        'paramiko'
    ],
    entry_points={
        'console_scripts': [
            'tuna=tuna.cli.main:main',
        ],
    },
)
