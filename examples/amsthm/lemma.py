#!/usr/bin/env python

"""
Pandoc filter to convert divs with class="lemma" to LaTeX
lemma environments in LaTeX output, and to numbered lemmas
in HTML output.
"""

from pandocfilters import toJSONFilter, RawBlock, Div

lemmacount = 0


def latex(x):
    return RawBlock('latex', x)


def html(x):
    return RawBlock('html', x)


def lemmas(key, value, format, meta):
    if key == 'Div':
        [[ident, classes, kvs], contents] = value
        if "lemma" in classes:
            if format == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return([latex('\\begin{lemma}' + label)] + contents +
                       [latex('\\end{lemma}')])
            elif format == "html" or format == "html5":
                global lemmacount
                lemmacount = lemmacount + 1
                newcontents = [html('<dt>Lemma ' + str(lemmacount) + '</dt>'),
                               html('<dd>')] + contents + [html('</dd>\n</dl>')]
                return Div([ident, classes, kvs], newcontents)

if __name__ == "__main__":
    toJSONFilter(lemmas)
