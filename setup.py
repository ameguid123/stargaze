# Credit https://github.com/pypa/sampleproject/blob/master/setup.py

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stargaze',
    version='0.1.0',
    description='View the location of celestial objects from the command-line',
    # TODO
    long_description=long_description,
    url='https://github.com/ameguid123/stargaze',
    author='Adham Meguid',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    # TODO
    keywords='astronomy command-line',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # TODO
    install_requires=[],
    extras_require={
    },

    # TODO
    package_data={
    },

    entry_points={
        'console_scripts': [
            'stargaze=stargaze.cli:main',
        ],
    },
)
