# Author: John MacFarlane <jgm@berkeley.edu>
# Copyright: (C) 2013 John MacFarlane
# License: BSD3

"""
Functions to aid writing python scripts that process the pandoc
AST serialized as JSON.
"""

import sys
import json

def walk(x, action, format, meta):
  """Walk a tree, applying an action to every object.
  Returns a modified tree.
  """
  if isinstance(x, list):
    array = []
    for item in x:
      if isinstance(item, dict):
        if item == {}:
          array.append(walk(item, action, format, meta))
        else:
          for k in item:
            res = action(k, item[k], format, meta)
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
  be replaced.  If it returns a list, the list will be spliced in to
  the list to which the target object belongs.  (So, returning an
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

def attributes(attrs):
  """Returns an attribute list, constructed from the
  dictionary attrs.
  """
  attrs = attrs or {}
  ident = attrs.get("id","")
  classes = attrs.get("classes",[])
  keyvals = [[x,attrs[x]] for x in attrs if (x != "classes" and x != "id")]
  return [ident, classes, keyvals]
