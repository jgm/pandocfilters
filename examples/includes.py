#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "include" and
replace their content with the included file
"""

from pandocfilters import toJSONFilter


def code_include(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, namevals], code] = value
        for nameval in namevals:
            if 'include' in nameval:
                with open(nameval[1], 'rb') as content_file:
                    content = unicode(content_file.read())
                return {'CodeBlock': [[ident, classes, namevals], content]}

if __name__ == "__main__":
    toJSONFilter(code_include)
