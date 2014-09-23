import os
from operator import itemgetter
from docutils import nodes
from docutils.parsers.rst import directives, Directive

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser import customization
from jinja2 import Environment, FileSystemLoader
from pelican import signals


class Publications(Directive):
    """ Embeds BibTeX publication list in document

    Usage:
    .. publications:: path/to/publications.bib
        :template: path/to/publications.html
        :sort: date

    where publications.bib is a bitex file.

    By default, pelican_publications looks for a publications.html template
    in the Pelican theme. Alternatively, the path to a template can be
    passed as an option.
    This template is a Jinja2 template that accepts a lists of bibtex entries.

    Possible sort options are:
        date: Sort by publication date descending (this is the default).
        key: Sort by bibtex key.
        name: Sort by author names.
    """

    def sort(argument):
        """ Option spec for sort option """
        return directives.choice(argument, ('key', 'date', 'name'))

    required_arguments = 1
    optional_arguments = 2
    has_content = False
    final_argument_whitespace = False
    option_spec = {
            'sort': sort,
            'template': directives.path,
            }

    def run(self):
        bibtex_path = self.arguments[0].strip()

        sort_type = self.options.get('sort', 'date')

        # Load the publications template
        if 'template' in self.options:
            template_path = self.options['template']
            template_dir, template_name = os.path.split(template_path)
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template(template_name)
        else:
            # Use template from the Pelican theme
            template = pelican_generator.get_template('publications')

        parser = BibTexParser()
        parser.customization = customize
        with open(bibtex_path, 'r') as bibtex_file:
            bib = bibtexparser.load(bibtex_file, parser=parser)

        entries = sort_entries(bib.entries, sort_type)

        rendered_template = template.render(publications=entries)
        return [nodes.raw('', rendered_template, format='html')]


def sort_entries(entries, sort_type):
    if sort_type == 'key':
        return sorted(entries, key=itemgetter('id'))
    elif sort_type == 'date':
        sort_key = lambda e: (
                int(e.get('year', 0)),
                month_ord(e.get('month', 'jan')))
        return sorted(entries, key=sort_key, reverse=True)
    elif sort_type == 'name':
        sort_key = lambda e: e.get('author', '')
        return sorted(entries, key=sort_key)
    else:
        raise ValueError("Invalid sort option: {0}".format(sort_type))


def month_ord(month_name):
    normalised_name = month_name[0:4].lower()
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    month_ords = dict((name, i) for i, name in enumerate(months))
    return month_ords[normalised_name]


def customize(record):
    """ Customise bibtexparser records
    """
    record = customization.convert_to_unicode(record)
    for field_name in ['author', 'title', 'journal']:
        try:
            field = record[field_name]
            record[field_name] = tex_to_html(field)
        except KeyError:
            pass
    # Splits author into a list of authors:
    record = customization.author(record)
    # Now convert each author into a tuple of last, first name
    record = split_authors(record)
    record = pages_endash(record)
    return record


def tex_to_html(tex):
    # Most characters are converted to unicode by
    # bibtexparser but some things
    # are missed, so fix them up here:
    return (tex
            .replace('\\&', '&amp;')
            .replace('\\o', u'\xf8')
            .replace('---', '&mdash;')
            .replace('--', '&ndash;')
            .replace('\\{', '&#123;')
            .replace('\\}', '&#125;')
            .replace('{', '')
            .replace('}', '')
            )


def split_authors(record):
    try:
        authors = record['author']
        record['author'] = [[n.strip() for n in a.split(',')] for a in authors]
    except KeyError:
        pass
    return record


def pages_endash(record):
    """ Convert pages to use an html en dash
    """
    try:
        # Convert to list of page numbers
        pages = [p.strip() for p in record['pages'].split('-')
                if p.strip()]
        record['pages'] = '&ndash;'.join(pages)
    except KeyError:
        pass
    return record


pelican_generator = None
def get_template_env(generator):
    global pelican_generator
    pelican_generator = generator


def register():
    # Register new RST directive
    directives.register_directive('publications', Publications)
    # Connect to Pelican generator init to get access
    # to the template environment.
    signals.generator_init.connect(get_template_env)
