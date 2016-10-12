#!/usr/bin/env python

"""
Pandoc filter to convert divs with latex="true" to LaTeX
environments in LaTeX output. The first class
will be regarded as the name of the latex environment
e.g.
<div latex="true" class="note abc">...</div>
will becomes
\begin{note}...\end{note}
"""

from pandocfilters import toJSONFilter, RawBlock, Div


def latex(x):
    return RawBlock('latex', x)


def latexdivs(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if ["latex","true"] in kvs:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{' + classes[0] + '}' + label)] + contents +
                       [latex('\\end{' + classes[0] + '}')])

if __name__ == "__main__":
    toJSONFilter(latexdivs)
