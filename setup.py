import sys
from setuptools import setup, find_packages

setup(
    name="bikeshares",
    version="0.0.0",
    description="Standardized access to the data published by bicycle sharing programs.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3"
    ],
    keywords="bikeshare citibike hubway divvy",
    author="Jeremy Singer-Vine",
    author_email="jsvine@gmail.com",
    url="http://github.com/buzzfeednews/bikeshares/",
    license="MIT",
    packages=find_packages(exclude=["test",]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        "pandas",
    ],
    tests_require=[],
    test_suite="test",
    entry_points={
        "console_scripts": [
        ]
    }
)
