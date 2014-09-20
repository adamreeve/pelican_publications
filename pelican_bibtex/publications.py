import os
from docutils import nodes
from docutils.parsers.rst import directives, Directive

import bibtexparser
from jinja2 import Environment, FileSystemLoader


class Publications(Directive):
    """ Embeds BibTeX publication list in document

    Usage:
    .. publications:: path/to/publications.bib path/to/publications.html
        :sort: date

    where publications.bib is a bitex file and publications.html
    is a Jinja2 template that accepts a lists of bibtex entries
    in the format used by the bibtexparser Python package.

    Possible sort options are:
        date: Sort by publication date (this is the default).
        key: Sort by bibtex key.
        name: Sort by author names.
    """

    def sort(argument):
        """ Option spec for sort option """
        return directives.choice(argument, ('key', 'date', 'name'))

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

        sort = self.options.get('sort', 'date')

        template_dir, template_name = os.path.split(template_path)
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)

        with open(bibtex_path, 'r') as bibtex_file:
            bib = bibtexparser.load(bibtex_file)

        rendered_template = template.render(publications=bib.entries)
        return [nodes.raw('', rendered_template, format='html')]


def register():
    directives.register_directive('publications', Publications)
