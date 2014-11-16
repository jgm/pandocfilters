#!/usr/bin/env python

"""
Pandoc filter to convert all regular text to uppercase.
Code, link URLs, etc. are not affected.
"""

from pandocfilters import toJSONFilter, Str


def caps(key, value, format, meta):
    if key == 'Str':
        return Str(value.upper())

if __name__ == "__main__":
    toJSONFilter(caps)
