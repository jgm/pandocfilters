#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="case" to LaTeX
case environments in LaTeX output, and to numbered cases
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

casecount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def cases(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "case" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{case}' + label)] + contents +
                       [latex('\\end{case}')])
            elif format == "html" or format == "html5":
                global casecount
                casecount = casecount + 1
                newcontents = [html('<dt>Case ' + str(casecount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(cases)
