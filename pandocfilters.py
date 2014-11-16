# Author: John MacFarlane <jgm@berkeley.edu>
# Copyright: (C) 2013 John MacFarlane
# License: BSD3

"""
Functions to aid writing python scripts that process the pandoc
AST serialized as JSON.
"""

import re
import sys
import json
from collections import OrderedDict


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
    """Converts an action into a filter that reads a JSON-formatted
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
    be replaced.    If it returns a list, the list will be spliced in to
    the list to which the target object belongs.    (So, returning an
    empty list deletes the object.)
    """
    doc = json.loads(sys.stdin.read())
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""
    altered = walk(doc, action, format, doc[0]['unMeta'])
    json.dump(altered, sys.stdout)


def stringify(x):
    """Walks the tree x and returns concatenated string content,
    leaving out all formatting.
    """
    result = []

    def go(key, val, format, meta):
        if key == 'Str':
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


def attributes(attrs={}):
    """Returns an attribute list, constructed from the
    dictionary attrs.
    """
    attr = Attributes(attrs, format='dict')
    return attr.to_pandoc()


class Attributes(object):
    """Parser / Emitter for pandoc block attributes.

    Can read and write attributes in any of these formats:
        - markdown
        - html
        - dictionary
        - pandoc

    usage:
        attrs = '#id .class1 .class2 key=value'
        attributes = PandocAttributes(attrs, format='markdown')

        attributes.to_markdown()
        >>> '{#id .class1 .class2 key=value}'

        attributes.to_dict()
        >>> {'id': 'id', 'classes': ['class1', 'class2'], 'key'='value'}

        attributes.to_html()
        >>> id="id" class="class1 class2" key='value'

        attributes.to_pandoc()
        >>> ['id', ['class1', 'class2'], [['key', 'value']]]

        attributes.id
        >>> 'id'

        attributes.classes
        >>> ['class1', 'class2']

        attributes.kvs
        >>> OrderedDict([('key', 'value')])
    """
    spnl = ' \n'
    split_regex = r'''((?:[^{separator}"']|"[^"]*"|'[^']*')+)'''.format

    def __init__(self, attr=None, format='pandoc'):
        if attr is None:
            id = ''
            classes = []
            kvs = OrderedDict()
        elif format == 'pandoc':
            id, classes, kvs = self.parse_pandoc(attr)
        elif format == 'markdown':
            id, classes, kvs = self.parse_markdown(attr)
        elif format == 'html':
            id, classes, kvs = self.parse_html(attr)
        elif format == 'dict':
            id, classes, kvs = self.parse_dict(attr)
        else:
            raise UserWarning('invalid format')

        self.id = id
        self.classes = classes
        self.kvs = kvs

    @classmethod
    def parse_pandoc(self, attrs):
        """Read pandoc attributes."""
        id = attrs[0]
        classes = attrs[1]
        kvs = OrderedDict(attrs[2])

        return id, classes, kvs

    @classmethod
    def parse_markdown(self, attr_string):
        """Read markdown attributes."""
        attr_string = attr_string.strip('{}')
        splitter = re.compile(self.split_regex(separator=self.spnl))
        attrs = splitter.split(attr_string)[1::2]

        # match single word attributes e.g. ```python
        if len(attrs) == 1 \
                and not attr_string.startswith(('#', '.')) \
                and '=' not in attr_string:
            return '', [attr_string], OrderedDict()

        try:
            id = [a[1:] for a in attrs if a.startswith('#')][0]
        except IndexError:
            id = ''

        classes = [a[1:] for a in attrs if a.startswith('.')]
        special = ['unnumbered' for a in attrs if a == '-']
        classes.extend(special)

        kvs = OrderedDict(a.split('=', 1) for a in attrs if '=' in a)

        return id, classes, kvs

    def parse_html(self, attr_string):
        """Read a html string to attributes."""
        splitter = re.compile(self.split_regex(separator=self.spnl))
        attrs = splitter.split(attr_string)[1::2]

        idre = re.compile(r'''id=["']?([\w ]*)['"]?''')
        clsre = re.compile(r'''class=["']?([\w ]*)['"]?''')

        id_matches = [idre.search(a) for a in attrs]
        cls_matches = [clsre.search(a) for a in attrs]

        try:
            id = [m.groups()[0] for m in id_matches if m][0]
        except IndexError:
            id = ''

        classes = [m.groups()[0] for m in cls_matches if m][0].split()

        special = ['unnumbered' for a in attrs if '-' in a]
        classes.extend(special)

        kvs = [a.split('=', 1) for a in attrs if '=' in a]
        kvs = OrderedDict((k, v) for k, v in kvs if k not in ('id', 'class'))

        return id, classes, kvs

    @classmethod
    def parse_dict(self, attrs):
        """Read a dict to attributes."""
        attrs = attrs or {}
        ident = attrs.get("id", "")
        classes = attrs.get("classes", [])
        kvs = OrderedDict((k, v) for k, v in attrs.items()
                          if k not in ("classes", "id"))

        return ident, classes, kvs

    def to_markdown(self, format='{id} {classes} {kvs}', surround=True):
        """Returns attributes formatted as markdown with optional
        format argument to determine order of attribute contents.
        """
        id = '#' + self.id if self.id else ''
        classes = ' '.join('.' + cls for cls in self.classes)
        kvs = ' '.join('{}={}'.format(k, v) for k, v in self.kvs.items())

        attrs = format.format(id=id, classes=classes, kvs=kvs).strip()

        if surround:
            return '{' + attrs + '}'
        elif not surround:
            return attrs

    def to_html(self):
        """Returns attributes formatted as html."""
        id, classes, kvs = self.id, self.classes, self.kvs
        id_str = 'id="{}"'.format(id) if id else ''
        class_str = 'class="{}"'.format(' '.join(classes)) if classes else ''
        key_str = ' '.join('{}={}'.format(k, v) for k, v in kvs.items())
        return ' '.join((id_str, class_str, key_str)).strip()

    def to_dict(self):
        """Returns attributes formatted as a dictionary."""
        d = {'id': self.id, 'classes': self.classes}
        d.update(self.kvs)
        return d

    def to_pandoc(self):
        kvs = [[k, v] for k, v in self.kvs.items()]
        return [self.id, self.classes, kvs]

    @property
    def markdown(self):
        return self.to_markdown()

    @property
    def html(self):
        return self.to_html()

    @property
    def dict(self):
        return self.to_dict()

    @property
    def list(self):
        return self.to_pandoc()

    @property
    def is_empty(self):
        return self.id == '' and self.classes == [] and self.kvs == {}

    def __getitem__(self, item):
        if item == 'id':
            return self.id
        elif item == 'classes':
            return self.classes
        else:
            return self.kvs.get(item) or {}

    def __setitem__(self, key, value):
        if key == 'id':
            self.id = value
        elif key == 'classes':
            self.classes = value
        else:
            self.kvs[key] = value

    def __repr__(self):
        return "pandocfilters.Attributes({})".format(self.to_pandoc())


def elt(eltType, numargs):
    def fun(*args):
        lenargs = len(args)
        if lenargs != numargs:
            raise ValueError(eltType + ' expects '
                             + str(numargs) + ' arguments, but given '
                             + str(lenargs))
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
Link = elt('Link', 2)
Image = elt('Image', 2)
Note = elt('Note', 1)
Span = elt('Span', 2)
