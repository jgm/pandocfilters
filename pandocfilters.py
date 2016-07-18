# Author: John MacFarlane <jgm@berkeley.edu>
# Copyright: (C) 2013 John MacFarlane
# License: BSD3

"""
Functions to aid writing python scripts that process the pandoc
AST serialized as JSON.
"""

import codecs
import hashlib
import io
import json
import os
import sys


# some utility-functions: make it easier to create your own filters


def get_filename4code(module, content, ext=None):
    """Generate filename based on content

    The function ensures that the (temporary) directory exists, so that the
    file can be written.

    Example:
        filename = get_filename4code("myfilter", code)
    """
    imagedir = module + "-images"
    fn = hashlib.sha1(content.encode(sys.getfilesystemencoding())).hexdigest()
    try:
        os.mkdir(imagedir)
        sys.stderr.write('Created directory ' + imagedir + '\n')
    except OSError:
        pass
    if ext:
        fn += "." + ext
    return os.path.join(imagedir, fn)


def get_caption(kv):
    """get caption from the keyvalues (options)

    Example:
      if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value
        caption, typef, keyvals = get_caption(keyvals)
        ...
        return Para([Image([ident, [], keyvals], caption, [filename, typef])])
    """
    res = []
    caption = []
    typef = ""
    for k, v in kv:
        if k == u"caption":
            caption = [Str(v)]
            typef = "fig:"
        else:
            res.append([k, v])

    return caption, typef, res


def get_extension(format, default, **alternates):
    """get the extension for the result, needs a default and some specialisations

    Example:
      filetype = get_extension(format, "png", html="svg", latex="eps")
    """
    try:
        return alternates[format]
    except KeyError:
        return default

# end of utilities


def walk(x, action, format, meta):
    """Walk a tree, applying an action to every object.
    Returns a modified tree.
    """
    if isinstance(x, list):
        array = []
        for item in x:
            if isinstance(item, dict) and 't' in item:
                res = action(item['t'], item['c'], format, meta)
                if res is None:
                    array.append(walk(item, action, format, meta))
                elif isinstance(res, list):
                    for z in res:
                        array.append(walk(z, action, format, meta))
                else:
                    array.append(walk(res, action, format, meta))
            else:
                array.append(walk(item, action, format, meta))
        return array
    elif isinstance(x, dict):
        obj = {}
        for k in x:
            obj[k] = walk(x[k], action, format, meta)
        return obj
    else:
        return x


def toJSONFilter(action):
    toJSONFilters([action])


def toJSONFilters(actions):
    """Generate a JSON-to-JSON filter

    The filter:

    * reads a JSON-formatted pandoc document from stdin
    * transforms it by walking the tree and performing the actions
    * returns a new JSON-formatted pandoc document to stdout

    The argument `actions` is a list of functions of the form
    `action(key, value, format, meta)`, where:

    * `key` is the type of the pandoc object (e.g. 'Str', 'Para') `value` is
    * the contents of the object (e.g. a string for 'Str', a list of
      inline elements for 'Para')
    * `format` is the target output format (which will be taken for the first
      command line argument if present)
    * `meta` is the document's metadata

    The return is either:

    * `None`: this means that the object should remain unchanged
    * a pandoc object: this will replace the original object
    * a list of pandoc objects: these will replace the original object; the
      list is merged with the neighbors of the orignal objects (spliced into
      the list the original object belongs to); returning an empty list deletes
      the object
    """
    try:
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    except AttributeError:
        # Python 2 does not have sys.stdin.buffer.
        # REF: https://stackoverflow.com/questions/2467928/python-unicodeencode
        input_stream = codecs.getreader("utf-8")(sys.stdin)

    doc = json.loads(input_stream.read())
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    altered = doc
    for action in actions:
        altered = walk(altered, action, format, doc[0]['unMeta'])

    json.dump(altered, sys.stdout)


def stringify(x):
    """Walks the tree x and returns concatenated string content,
    leaving out all formatting.
    """
    result = []

    def go(key, val, format, meta):
        if key in ['Str', 'MetaString']:
            result.append(val)
        elif key == 'Code':
            result.append(val[1])
        elif key == 'Math':
            result.append(val[1])
        elif key == 'LineBreak':
            result.append(" ")
        elif key == 'Space':
            result.append(" ")

    walk(x, go, "", {})
    return ''.join(result)


def attributes(attrs):
    """Returns an attribute list, constructed from the
    dictionary attrs.
    """
    attrs = attrs or {}
    ident = attrs.get("id", "")
    classes = attrs.get("classes", [])
    keyvals = [[x, attrs[x]] for x in attrs if (x != "classes" and x != "id")]
    return [ident, classes, keyvals]


def elt(eltType, numargs):
    def fun(*args):
        lenargs = len(args)
        if lenargs != numargs:
            raise ValueError(eltType + ' expects ' + str(numargs) +
                             ' arguments, but given ' + str(lenargs))
        if numargs == 0:
            xs = []
        elif len(args) == 1:
            xs = args[0]
        else:
            xs = args
        return {'t': eltType, 'c': xs}
    return fun

# Constructors for block elements

Plain = elt('Plain', 1)
Para = elt('Para', 1)
CodeBlock = elt('CodeBlock', 2)
RawBlock = elt('RawBlock', 2)
BlockQuote = elt('BlockQuote', 1)
OrderedList = elt('OrderedList', 2)
BulletList = elt('BulletList', 1)
DefinitionList = elt('DefinitionList', 1)
Header = elt('Header', 3)
HorizontalRule = elt('HorizontalRule', 0)
Table = elt('Table', 5)
Div = elt('Div', 2)
Null = elt('Null', 0)

# Constructors for inline elements

Str = elt('Str', 1)
Emph = elt('Emph', 1)
Strong = elt('Strong', 1)
Strikeout = elt('Strikeout', 1)
Superscript = elt('Superscript', 1)
Subscript = elt('Subscript', 1)
SmallCaps = elt('SmallCaps', 1)
Quoted = elt('Quoted', 2)
Cite = elt('Cite', 2)
Code = elt('Code', 2)
Space = elt('Space', 0)
LineBreak = elt('LineBreak', 0)
Math = elt('Math', 2)
RawInline = elt('RawInline', 2)
Link = elt('Link', 3)
Image = elt('Image', 3)
Note = elt('Note', 1)
SoftBreak = elt('SoftBreak', 0)
Span = elt('Span', 2)
