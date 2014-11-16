import nose.tools as nt

from collections import OrderedDict

from pandocfilters import Attributes, attributes


attr_markdown = r"""{#identify .class1 .class2 .unnumbered
key1=blah key2="o'brien = 1"}"""

attr_markdown_special = r"""{#identify .class1 .class2
key1=blah key2="o'brien = 1" -}"""

attr_dict = OrderedDict()
attr_dict['id'] = 'identify'
attr_dict['classes'] = ['class1', 'class2', 'unnumbered']
attr_dict['key1'] = 'blah'
attr_dict['key2'] = '"o\'brien = 1"'

attr_html = ('''id="identify" '''
             '''class="class1 class2 unnumbered" '''
             '''key1=blah key2="o'brien = 1"''')

attr_pandoc = ['identify',
               ['class1', 'class2', 'unnumbered'],
               [['key1', 'blah'],
                ['key2', '"o\'brien = 1"']]
               ]


def test_original():
    """Check that the original behaviour of pandocfilters.attributes
    is the same.
    """
    assert(attributes(attr_dict) == attr_pandoc)


def test_markdown():
    attr = Attributes(attr_markdown, 'markdown')

    print attr_dict
    print attr.to_dict()
    nt.assert_dict_equal(attr_dict, attr.to_dict())
    nt.assert_equal(attr_html, attr.to_html())
    nt.assert_equal(attr_markdown.replace('\n', ' '), attr.to_markdown())
    assert(attr_pandoc == attr.to_pandoc())


def test_html():
    attr = Attributes(attr_html, 'html')

    print attr_dict
    print attr.to_dict()
    nt.assert_dict_equal(attr_dict, attr.to_dict())
    nt.assert_equal(attr_html, attr.to_html())
    nt.assert_equal(attr_markdown.replace('\n', ' '), attr.to_markdown())
    assert(attr_pandoc == attr.to_pandoc())


def test_dict():
    attr = Attributes(attr_dict, 'dict')

    print attr_dict
    print attr.to_dict()
    nt.assert_dict_equal(attr_dict, attr.to_dict())
    nt.assert_equal(attr_html, attr.to_html())
    nt.assert_equal(attr_markdown.replace('\n', ' '), attr.to_markdown())
    assert(attr_pandoc == attr.to_pandoc())


def test_pandoc():
    attr = Attributes(attr_pandoc, 'pandoc')

    print attr_dict
    print attr.to_dict()
    nt.assert_dict_equal(attr_dict, attr.to_dict())
    nt.assert_equal(attr_html, attr.to_html())
    nt.assert_equal(attr_markdown.replace('\n', ' '), attr.to_markdown())
    assert(attr_pandoc == attr.to_pandoc())


def test_markdown_special():
    attr = Attributes(attr_markdown, 'markdown')
    attr_special = Attributes(attr_markdown_special, 'markdown')

    assert(attr.id == attr_special.id)
    assert(attr.classes == attr_special.classes)
    assert(attr.kvs == attr_special.kvs)


def test_markdown_single():
    attr = Attributes('python', 'markdown')

    assert(attr.id == '')
    assert(attr.classes == ['python'])
    assert(attr.kvs == OrderedDict())


def test_empty():
    attr = Attributes()
    assert attr.is_empty


def test_getitem():
    attr = Attributes()
    assert attr['id'] == ''
    assert attr['classes'] == []
    assert not attr['whatever']
    attr.kvs['whatever'] = 'dude'
    assert attr['whatever'] == 'dude'


def test_markdown_format():
    attr = Attributes()
    attr.id = 'a'
    attr.classes = ['b']
    attr.kvs['c'] = 'd'

    md = attr.to_markdown(format='{classes} {id} {kvs}')
    assert(md == '{.b #a c=d}')


def test_properties():
    attr = Attributes(attr_markdown, 'markdown')
    assert(attr.html == attr.to_html())
    assert(attr.markdown == attr.to_markdown())
    assert(attr.dict == attr.to_dict())
    assert(attr.list == attr.to_pandoc())


def test_surround():
    attr = Attributes(attr_markdown, 'markdown')
    print attr.to_markdown(surround=False)
    print attr_markdown.replace('\n', ' ').strip('{}')
    assert(attr.to_markdown(surround=False)
           == attr_markdown.replace('\n', ' ').strip('{}'))
