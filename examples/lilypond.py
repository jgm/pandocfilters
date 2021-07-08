#!/usr/bin/env python3

"""
Pandoc filter to process code blocks with class "ly" containing
Lilypond notation.  Assumes that Lilypond and Ghostscript are
installed, plus [lyluatex](https://github.com/jperon/lyluatex) package for
LaTeX, with LuaLaTeX.
"""

import os
from sys import getfilesystemencoding, stderr
from subprocess import Popen, call, PIPE
from hashlib import sha1
from pandocfilters import toJSONFilter, stringify,\
    Para, Image, RawInline, RawBlock

IMAGEDIR = "tmp_ly"
LATEX_DOC = """\\documentclass{article}
\\usepackage{libertine}
\\usepackage{lyluatex}
\\pagestyle{empty}
\\begin{document}
%s
\\end{document}
"""


def sha(x):
    return sha1(x.encode(getfilesystemencoding())).hexdigest()


def latex(code):
    """LaTeX inline"""
    return RawInline('latex', code)


def latexblock(code):
    """LaTeX block"""
    return RawBlock('latex', code)


def ly2png(lily, outfile, kvs):
    p = Popen([
        "lilypond",
        "-dno-point-and-click",
        "-dbackend=eps",
        "-djob-count=2",
        "-ddelete-intermediate-files",
        "-o", outfile,
        "-"
    ], stdin=PIPE, stdout=stderr)
    p.stdin.write(("\\paper{\n"
        "indent=0\\mm\n"
        "oddFooterMarkup=##f\n"
        "oddHeaderMarkup=##f\n"
        "bookTitleMarkup = ##f\n"
        "scoreTitleMarkup = ##f\n"
        "line-width = %s\n"
        "}\n"
        "#(set-global-staff-size %s)\n" % (
            kvs['width'][:-2] + '\\' + kvs['width'][-2:],
            kvs['staffsize']) +
        lily).encode("utf-8"))
    p.communicate()
    p.stdin.close()
    call([
        "gs",
        "-sDEVICE=pngalpha",
        "-r144",
        "-sOutputFile=" + outfile + '.png',
        outfile + '.pdf',
    ], stdout=stderr)


def png(contents, kvs):
    """Creates a png if needed."""
    outfile = os.path.join(IMAGEDIR, sha(contents + str(kvs['staffsize'])))
    src = outfile + '.png'
    if not os.path.isfile(src):
        try:
            os.mkdir(IMAGEDIR)
            stderr.write('Created directory ' + IMAGEDIR + '\n')
        except OSError:
            pass
        ly2png(contents, outfile, kvs)
        stderr.write('Created image ' + src + '\n')
    return src


def calc_params(kvs, meta):
    if 'staffsize' not in kvs:
        try:
            kvs['staffsize'] = int(
                meta['music']['c']['lilypond']['c']['staffsize']['c']
            )
        except (KeyError, TypeError):
            kvs['staffsize'] = 20
    if 'width' not in kvs:
        try:
            kvs['width'] = \
                meta['music']['c']['lilypond']['c']['width']['c'][0]['c']
        except (KeyError, TypeError):
            kvs['width'] = '210mm'
    return kvs


def lily(key, value, fmt, meta):
    if key == 'Code':
        [[ident, classes, kvs], contents] = value  # pylint:disable=I0011,W0612
        kvs = {key: value for key, value in kvs}
        if "ly" in classes:
            kvs = calc_params(kvs, meta)
            if fmt == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return latex(
                    '\\includely[staffsize=%s]{%s}' % (
                        kvs['staffsize'], contents
                    ) +
                    label
                )
            else:
                infile = contents + (
                    '.ly' if '.ly' not in contents else ''
                )
                with open(infile, 'r') as doc:
                    code = doc.read()
                return [
                    Image(['', [], []],
                        [],
                        [png(code, kvs), ""]
                    )
                ]
    if key == 'CodeBlock':
        [[ident, classes, kvs], code] = value
        kvs = {key: value for key, value in kvs}
        if "ly" in classes:
            kvs = calc_params(kvs, meta)
            if fmt == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return latexblock(
                    '\\lily[staffsize=%s]{%s}' % (kvs['staffsize'], code) +
                    label
                )
            else:
                return Para([
                    Image(
                        ['', [], []],
                        [],
                        [png(code, kvs), ""]
                    )
                ])

if __name__ == "__main__":
    toJSONFilter(lily)
