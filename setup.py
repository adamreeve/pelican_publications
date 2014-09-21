import os

from setuptools import setup


def read_version():
    here = os.path.abspath(os.path.dirname(__file__))
    version_path = os.path.sep.join(
            (here, "pelican_publications", "version.py"))
    v_globals = {}
    v_locals = {}
    exec(open(version_path).read(), v_globals, v_locals)
    return v_locals['__version__']


setup(
  name = 'pelican_publications',
  version = read_version(),
  description = ("A Pelican plugin that adds an RST directive for including a BibTeX publication list."),
  author = 'Adam Reeve',
  author_email = 'adreeve@gmail.com',
  url = 'https://github.com/adamreeve/pelican_publications',
  packages = ['pelican_publications'],
  long_description=open('README.rst').read(),
  license = 'MIT',
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Intended Audience :: Developers',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Text Processing',
  ],
  install_requires = ['bibtexparser'],
)
