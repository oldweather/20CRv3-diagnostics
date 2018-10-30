"""Setup configuration for the 20CRv3 package.

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open  # 2.7 only
import glob

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='20CRv3',
    version='0.0.1',
    description='Analyses of 20CRv3 ',

    # From README - see above
    long_description=long_description,
    #long_description_content_type='text/x-rst',

    url='https://brohan.org/20CRv3-diagnostics/',

    author='Philip Brohan',
    author_email='philip.brohan@metofice.gov.uk',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],

    # Keywords for your project. What does your project relate to?
    keywords='weather observations assimilation',

    # Automatically find the software to be included
    package_dir = {'': 'modules'},
    packages=find_packages(where='modules'),


    # Other packages that your project depends on.
    install_requires=[
        'IRData>0.0',
        'Meteorographica>0.0',
        'numpy>=1.15.2',
        'scipy>=1.1.0',
        'pandas>=0.23.4',
        'scikit-learn>0.19',
        'matplotlib==2.2.3',
    ],


)
