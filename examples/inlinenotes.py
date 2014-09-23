#!/usr/bin/env python
 
from pandocfilters import toJSONFilter, RawInline, Str, Space
 
"""
Pandoc filter for Markdown output that converts all notes to Pandoc
Markdown's inline notes. If notes had multiple paragraphs in the input,
the paragraphs are joined by a single space in the new inline note.
"""
 
def inlinenotes(k, v, f, meta):
  if k == 'Note' and f == 'markdown':
    vlist = v[0]['c']
    for d in v[1:]:
       vlist.append(Space())
       vlist.extend(d['c'])
    # use RawInline to avoid backslash escape of '^' in Markdown output
    return [RawInline('html', '^[')] + vlist + [Str(']')]
 
if __name__ == "__main__":
  toJSONFilter(inlinenotes)
