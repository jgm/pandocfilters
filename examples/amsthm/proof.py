#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="proof" to LaTeX
proof environments in LaTeX output, and to numbered proofs
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

proofcount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def proofs(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "proof" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{proof}' + label)] + contents +
                       [latex('\\end{proof}')])
            elif format == "html" or format == "html5":
                global proofcount
                proofcount = proofcount + 1
                newcontents = [html('<dt>Proof ' + str(proofcount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(proofs)
