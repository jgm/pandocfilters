#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="remark" to LaTeX
remark environments in LaTeX output, and to numbered remarks
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

remarkcount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def remarks(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "remark" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{remark}' + label)] + contents +
                       [latex('\\end{remark}')])
            elif format == "html" or format == "html5":
                global remarkcount
                remarkcount = remarkcount + 1
                newcontents = [html('<dt>Remark ' + str(remarkcount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(remarks)
