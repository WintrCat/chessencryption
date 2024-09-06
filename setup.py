from setuptools import setup, find_packages

setup(
    name='chessencryption',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'chess',
        'flask'
    ]
)