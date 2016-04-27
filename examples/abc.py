#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "abc" containing
ABC notation into images.  Assumes that abcm2ps and ImageMagick's
convert are in the path.  Images are put in the abc-images directory.
"""

import os
import sys
from subprocess import Popen, PIPE, call

from pandocfilters import toJSONFilter, Para, Image, get_caption, get_filename4code, get_extension


def abc2eps(abc_src, filetype, outfile):
    p = Popen(["abcm2ps", "-O", outfile + '.eps', "-"], stdin=PIPE)
    p.stdin.write(abc_src)
    p.communicate()
    p.stdin.close()
    call(["convert", outfile + '.eps', outfile + '.' + filetype])


def abc(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value
        if "abc" in classes:
            caption, typef, keyvals = get_caption(keyvals)
            outfile = get_filename4code("abc", code)
            filetype = get_extension(format, "png", html="png", latex="pdf")
            dest = outfile + '.' + filetype

            if not os.path.isfile(dest):
                abc2eps(code.encode("utf-8"), filetype, outfile)
                sys.stderr.write('Created image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])


if __name__ == "__main__":
    toJSONFilter(abc)
