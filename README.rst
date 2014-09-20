A plugin for the Pelican_ static website generator that
embeds a BibTeX publication list in a page or article
using a ``publications`` restructured text directive.

Usage::

    .. publications:: path/to/publications.bib path/to/publications.html
        :sort: date

In this example, publications.bib is a BibTeX file and publications.html
is a Jinja2 template that accepts a lists of BibTeX entries.
These BibTeX entries are dictionaries
in the format used by the bibtexparser_ Python package.

Possible sort options are:

date
    Sort by publication date (this is the default).

key
    Sort by BibTeX key.

name
    Sort by author names.

.. _Pelican: http://docs.getpelican.com
.. _bibtexparser: https://bibtexparser.readthedocs.org
