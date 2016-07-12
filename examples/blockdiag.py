#!/usr/bin/env python

"""
Filter to process code blocks with class "blockdiag" into
generated images.

Needs utils from http://blockdiag.com
"""

import os
import sys
from subprocess import call

from pandocfilters import toJSONFilter, Para, Image, get_filename4code, get_caption, get_extension


def blockdiag(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "blockdiag" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("blockdiag", code)
            filetype = get_extension(format, "png", html="svg", latex="pdf")

            src = filename + '.diag'
            dest = filename + '.' + filetype

            if not os.path.isfile(dest):
                txt = code.encode(sys.getfilesystemencoding())
                with open(src, "w") as f:
                    f.write(txt)

                call(["blockdiag", "-a", "-T"+filetype, src])
                sys.stderr.write('Created image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(blockdiag)
