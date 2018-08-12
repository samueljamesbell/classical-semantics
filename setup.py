import os
from setuptools import find_packages, setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "classical-semantics",
    version = "0.0.1",
    author = "Samuel Bell",
    author_email = "samueljamesbell@gmail.com",
    description = "Experiments in classical music recommendation.",
    license = "MIT",
    packages=find_packages(),
    long_description=read('README.md'),
    entry_points = {
        'console_scripts': [
            'fetch-wikipedia-entries=composer2vec.script.fetch_wikipedia_entries:main',
        ],
    }
)
