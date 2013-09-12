pandocfilters
=============

A python module for writing pandoc filters.  Pandoc filters
are pipes that read a JSON serialization of the Pandoc AST
from stdin, transform it in some way, and write it to stdout.
They can be used with pandoc (>= 1.12) either using pipes:::

    pandoc -t json -s | ./caps.py | pandoc -f json

or using the ``--filter`` (or ``-F``) command-line option:::

    pandoc --filter ./caps.py -s

For more on pandoc filters, see the pandoc documentation under ``--filter``
and `the tutorial on writing filters`__.

__ http://johnmacfarlane.net/pandoc/scripting.html

To install::

    python setup.py install

The source repository contains a number of illustrative examples
in the ``examples`` subdirectory.

The ``pandocfilters`` module exports the following functions:

``walk(x, action, format, meta)``
  Walk a tree, applying an action to every object.
  Returns a modified tree.

``toJSONFilter(action)``
  Converts an action into a filter that reads a JSON-formatted
  pandoc document from stdin, transforms it by walking the tree
  with the action, and returns a new JSON-formatted pandoc document
  to stdout.  The argument is a function action(key, value, format, meta),
  where key is the type of the pandoc object (e.g. 'Str', 'Para'),
  value is the contents of the object (e.g. a string for 'Str',
  a list of inline elements for 'Para'), format is the target
  output format (which will be taken for the first command line
  argument if present), and meta is the document's metadata.
  If the function returns None, the object to which it applies
  will remain unchanged.  If it returns an object, the object will
  be replaced.  If it returns a list, the list will be spliced in to
  the list to which the target object belongs.  (So, returning an
  empty list deletes the object.)

``stringify(x)``
  Walks the tree ``x`` and returns concatenated string content,
  leaving out all formatting.

``attributes(attrs)``
  Returns an attribute list, constructed from the
  dictionary ``attrs``.

Most users will only need ``toJSONFilter``.  Here is a simple example
of its use:::

    #!/usr/bin/env python

    """
    Pandoc filter to convert all regular text to uppercase.
    Code, link URLs, etc. are not affected.
    """

    from pandocfilters import toJSONFilter

    def caps(key, value, format, meta):
      if key == 'Str':
        return {'Str': value.upper()}

    if __name__ == "__main__":
      toJSONFilter(caps)

