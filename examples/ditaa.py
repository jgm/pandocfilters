#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "ditaa" into images.

Needs `ditaa.jar` from http://ditaa.sourceforge.net/.
"""

import os
import sys
import pprint
from subprocess import call

from pandocfilters import toJSONFilter, Para, Image, get_filename4code, get_caption, get_extension


def ditaa(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "ditaa" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("ditaa", code)
            filetype = get_extension(format, "png", html="svg", latex="eps")

            src = filename + '.txt'
            dest = filename + '.' + filetype

            if not os.path.isfile(dest):
                with open(src, "w") as f:
                    f.write(code)

                call(["java", "-jar", "ditaa.jar", src])
                pprint.pprint(['Created image ', dest, 'typef=', typef, 'ident=', ident,  'keyvals=', keyvals, 'caption=', caption], sys.stderr)

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(ditaa)
