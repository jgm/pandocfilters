#!/usr/bin/env python
from pandocfilters import walk, toJSONFilter
from caps import caps

"""
Pandoc filter that causes emphasized text to be displayed
in ALL CAPS.
"""


def deemph(key, val, fmt, meta):
    if key == 'Emph':
        return walk(val, caps, fmt, meta)

if __name__ == "__main__":
    toJSONFilter(deemph)
