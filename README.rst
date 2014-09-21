A plugin for the Pelican_ static website generator that
embeds a BibTeX publication list in a page or article
using a ``publications`` restructured text directive.

Usage::

    .. publications:: path/to/publications.bib
        :template: path/to/publications.html
        :sort: date

By default pelican_publications uses a ``publications`` template
in the Pelican theme. This can be overridden by setting
the template option as a path to a Jinja2 template.
The template is passed one parameter, ``publications``, which is
a list of BibTeX entries.
These BibTeX entries are simple dictionaries
in the format used by the bibtexparser_ Python package, with a few
customisations such as converting page ranges to use an html en dash
and splitting the author field into a list of authors.

Possible sort options are:

date
    Sort by publication date (this is the default).

key
    Sort by BibTeX key.

name
    Sort by author names.

.. _Pelican: http://docs.getpelican.com
.. _bibtexparser: https://bibtexparser.readthedocs.org
