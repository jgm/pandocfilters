#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="corollary" to LaTeX
corollary environments in LaTeX output, and to numbered corollarys
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

corollarycount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def corollarys(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "corollary" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{corollary}' + label)] + contents +
                       [latex('\\end{corollary}')])
            elif format == "html" or format == "html5":
                global corollarycount
                corollarycount = corollarycount + 1
                newcontents = [html('<dt>Corollary ' + str(corollarycount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(corollarys)
