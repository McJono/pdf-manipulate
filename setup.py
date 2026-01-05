#!/usr/bin/env python3
"""
PDF Manipulate - Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-manipulate",
    version="0.1.0",
    author="McJono",
    description="An intelligent PDF manipulation program that automates document processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/McJono/pdf-manipulate",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyPDF2>=3.0.0",
        "PyMuPDF>=1.23.0",
        "Pillow>=10.0.0",
        "pdf2image>=1.16.0",
        "pytesseract>=0.3.10",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "pylint>=2.17.0",
            "mypy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pdf-manipulate=main:main",
        ],
    },
)
