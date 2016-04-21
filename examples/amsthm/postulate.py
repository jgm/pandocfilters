#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="postulate" to LaTeX
postulate environments in LaTeX output, and to numbered postulates
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

postulatecount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def postulates(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "postulate" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{postulate}' + label)] + contents +
                       [latex('\\end{postulate}')])
            elif format == "html" or format == "html5":
                global postulatecount
                postulatecount = postulatecount + 1
                newcontents = [html('<dt>Postulate ' + str(postulatecount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(postulates)
