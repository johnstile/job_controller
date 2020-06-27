#
# create python package from source found in 'src' directory
#
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Store the service's version in version['__version__'].
#version = {}
#
#with open(os.path.join(here, "web", "_version.py")) as ver_file:
#    exec(ver_file.read(), version)

install_requires = [
  "Flask>=1.1.1",
  "Flask-Cors>=3.0.8",
  "flask_redis>=0.4.0"
] 

setup_requires = []

tests_require = [
    "boto3>=1.7.84",
    "botocore>=1.10.84",
    "moto>=1.3.6",
    "pytest>=5.4.3",
    "pytest-cov>=2.10.0",
    "pytest-mock>=3.1.1",
    "pytest-sugar>=0.9.3",
]

extras_require = {
    "dev": [
        # flake8 must appear before autopep8 to avoid a bug in pycodestyle
        "flake8",
        "autopep8",
        "sphinx",
    ]
    + tests_require
}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="web",
    version="0.0.1",
    author="John Stile",
    author_email="john@stilen.com",
    description="App Bundle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["service"],
    install_requires=install_requires,
    extras_require=extras_require,
    setup_requires=setup_requires,
    tests_require=tests_require,
    package_dir={"": "src"},
    packages=find_packages("src"),
    package_data={'': ['flask.cfg']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
