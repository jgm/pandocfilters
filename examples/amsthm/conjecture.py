#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="conjecture" to LaTeX
conjecture environments in LaTeX output, and to numbered conjectures
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

conjecturecount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def conjectures(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "conjecture" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{conjecture}' + label)] + contents +
                       [latex('\\end{conjecture}')])
            elif format == "html" or format == "html5":
                global conjecturecount
                conjecturecount = conjecturecount + 1
                newcontents = [html('<dt>Conjecture ' + str(conjecturecount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(conjectures)
