#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="proposition" to LaTeX
proposition environments in LaTeX output, and to numbered propositions
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

propositioncount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def propositions(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "proposition" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{proposition}' + label)] + contents +
                       [latex('\\end{proposition}')])
            elif format == "html" or format == "html5":
                global propositioncount
                propositioncount = propositioncount + 1
                newcontents = [html('<dt>Proposition ' + str(propositioncount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(propositions)
