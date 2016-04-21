#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="example" to LaTeX
example environments in LaTeX output, and to numbered examples
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

examplecount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def examples(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "example" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{example}' + label)] + contents +
                       [latex('\\end{example}')])
            elif format == "html" or format == "html5":
                global examplecount
                examplecount = examplecount + 1
                newcontents = [html('<dt>Example ' + str(examplecount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(examples)
