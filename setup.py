from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description = f.read()

setup(
    name='chessencryption',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'chess',
        'flask'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)