#!/usr/bin/env python3

from pandocfilters import toJSONFilter, Math, Para
"""
Pandoc filter to convert gitlab flavored markdown to pandoc flavored markdown
"""


def gitlab_markdown(key, value, format, meta):
    if key == "CodeBlock":
        [[identification, classes, keyvals], code] = value
        if len(classes) > 0 and classes[0] == "math":
            fmt = {'t': 'DisplayMath',
                   'c': []}
            return Para([Math(fmt, code)])

    elif key == "Math":
        [fmt, code] = value
        if isinstance(fmt, dict) and fmt['t'] == "InlineMath":
            # if fmt['t'] == "InlineMath":
            return Math(fmt, code.strip('`'))


if __name__ == "__main__":
    toJSONFilter(gitlab_markdown)
