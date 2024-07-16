"""

Pip Setup for Tuna

"""

# pylint: disable=all

from setuptools import setup, find_packages

setup(
    name='tuna-cli',
    version='0.1.2',
    author='Abhigyan Arya (Opennote Labs)',
    author_email='support@opennote.me',
    description='Fine tuning, reimagined. Welcome to tuna - we\'re simplifying cloud compute architecture, datasets, and more, to get your specialized AI from 0 to 1 ASAP.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/abhi-arya1/tuna',
    project_urls={
        'Homepage': 'https://github.com/abhi-arya1/tuna',
        'Issues': 'https://github.com/abhi-arya1/tuna/issues',
    },
    packages=find_packages(include=['tuna', 'tuna.*']),
    python_requires='>=3.12',
    install_requires=[
        'inquirer',
        'requests',
        'halo',
        'jupyterlab',
        'nbformat',
        'scikit-learn',
        'tabulate',
        'paramiko',
        'transformers'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
)
