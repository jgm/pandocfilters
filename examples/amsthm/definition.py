#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="definition" to LaTeX
definition environments in LaTeX output, and to numbered definitions
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

definitioncount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def definitions(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "definition" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{definition}' + label)] + contents +
                       [latex('\\end{definition}')])
            elif format == "html" or format == "html5":
                global definitioncount
                definitioncount = definitioncount + 1
                newcontents = [html('<dt>Definition ' + str(definitioncount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(definitions)
