import os
from docutils import nodes
from docutils.parsers.rst import directives, Directive

import bibtexparser
import jinja2


class Publications(Directive):
    """ Embeds BibTeX publication list in document

    Usage:
    .. publications:: path/to/publications.bib path/to/publications.html
        :sort: date

    where publications.bib is a bitex file and publications.html
    is a Jinja2 template that accepts a lists of bibtex entries
    in the format used by the bibtexparser Python package.
    Possible sort options are:
        date: Sort by date (this is the default).
        none: Use sorting in BibTeX file.
        name: Sort by author names.
    """

    def sort(argument):
        """ Option spec for sort option """
        return directives.choice(argument, ('none', 'date', 'name'))

    required_arguments = 2
    optional_arguments = 1
    has_content = False
    final_argument_whitespace = False
    option_spec = {
            'sort': sort,
            }

    def run(self):
        bibtex_path = self.arguments[0].strip()
        template_path = self.arguments[1].strip()

        sort = self.options.get('sort', 'not_given')

        return [nodes.raw('', "<p>Testing publications plugin. Got arguments:</p>"
                "<ul><li>bibtex_path = %s</li><li>template_path = %s</li>"
                "<li>Current dir: %s</li>"
                "<li>Sort option: %s</li>"
                "</ul>" % (bibtex_path, template_path, os.getcwd(), sort),
                format='html')]


def register():
    directives.register_directive('publications', Publications)
