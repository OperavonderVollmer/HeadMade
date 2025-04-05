from setuptools import setup, find_packages

setup(
    name="HeadMade",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "OperaPowerRelay @ git+https://github.com/OperavonderVollmer/OperaPowerRelay.git",
    ],
    python_requires=">=3.7",
    author="Opera von der Vollmer",
    description="Simple house cleaner for file systems",
    url="https://github.com/OperavonderVollmer/HeadMade", 
    license="MIT",
)
