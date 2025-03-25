from setuptools import setup, find_packages

setup(
    name="FileWhisperer",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pytaglib",
        "python-magic-bin",
        "pillow",
        "deep-translator",
        "OperaPowerRelay @ git+https://github.com/OperavonderVollmer/OperaPowerRelay.git@v1.1.2",
        "FileWhisperer @ git+https://github.com/OperavonderVollmer/FileWhisperer@main",
    ],
    python_requires=">=3.7",
    author="Opera von der Vollmer",
    description="Script for manipulating metadata of files",
    url="https://github.com/OperavonderVollmer/FileWhisperer", 
    license="MIT",
)
