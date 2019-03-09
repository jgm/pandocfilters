#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "graphviz" into
graphviz-generated images.

Needs pygraphviz
"""

import os
import sys
import string

import pygraphviz

from pandocfilters import toJSONFilter, Para, Image, get_filename4code, get_caption, get_extension, get_value

def graphviz(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value
        if "graphviz" in classes:
            caption, typef, keyvals = get_caption(keyvals)
            prog, keyvals = get_value(keyvals, u"prog", u"dot")
            filetype = get_extension(format, "png", html="png", latex="pdf")
            dest = get_filename4code("graphviz", code, filetype)
            filename = ""
            for a,fname in keyvals:
                if(a == "filename"):
                    valid_chars = "-_ %s%s" % (string.ascii_letters, string.digits)
                    fname = ''.join(x for x in fname if x in valid_chars)
                    if fname != "":
                        filename = "graphviz-images/"+fname+"."+filetype
                        dest = filename
            if (filename != "") or (not os.path.isfile(dest)):
                g = pygraphviz.AGraph(string=code)
                g.layout()
                g.draw(dest, prog=prog)
                sys.stderr.write('Created image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(graphviz)
