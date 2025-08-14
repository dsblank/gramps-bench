#!/usr/bin/env python3
"""
Setup script for gramps-bench package
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="gramps-bench",
    version="1.0.0",
    author="Gramps Development Team",
    author_email="gramps-devel@lists.sourceforge.net",
    description="Performance benchmarking tools for Gramps genealogy software",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/gramps-project/gramps-benchmarks",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=6.0",
        "pytest-benchmark>=3.4",
        "matplotlib>=3.3",
        "numpy>=1.19",
    ],
    entry_points={
        "console_scripts": [
            "gramps-bench=gramps_bench.cli.gramps_bench:main",
            "gramps-bench-all=gramps_bench.cli.gramps_bench_all:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 
