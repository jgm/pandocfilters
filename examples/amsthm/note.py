#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="note" to LaTeX
note environments in LaTeX output, and to numbered notes
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

notecount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def notes(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "note" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{note}' + label)] + contents +
                       [latex('\\end{note}')])
            elif format == "html" or format == "html5":
                global notecount
                notecount = notecount + 1
                newcontents = [html('<dt>Note ' + str(notecount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(notes)
