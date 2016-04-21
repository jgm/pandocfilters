#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="problem" to LaTeX
problem environments in LaTeX output, and to numbered problems
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

problemcount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def problems(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "problem" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{problem}' + label)] + contents +
                       [latex('\\end{problem}')])
            elif format == "html" or format == "html5":
                global problemcount
                problemcount = problemcount + 1
                newcontents = [html('<dt>Problem ' + str(problemcount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(problems)
