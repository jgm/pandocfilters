#!/usr/bin/env python3
"""
Pandoc filter to convert code blocks with class "gabc" to LaTeX
\\gabcsnippet commands in LaTeX output, and to images in HTML output.
Assumes Ghostscript, LuaLaTeX, [Gregorio](http://gregorio-project.github.io/)
and a reasonable selection of LaTeX packages are installed.
"""

import os
from sys import getfilesystemencoding, stderr
from subprocess import Popen, call, PIPE, DEVNULL
from hashlib import sha1
from pandocfilters import toJSONFilter, RawBlock, RawInline, Para, Image


STDERR = DEVNULL
IMAGEDIR = "tmp_gabc"
LATEX_DOC = """\\documentclass{article}
\\usepackage{libertine}
\\usepackage[autocompile,allowdeprecated=false]{gregoriotex}
\\catcode`\\℣=\\active \\def ℣#1{{\\Vbar\\hspace{-.25ex}#1}}
\\catcode`\\℟=\\active \\def ℟#1{{\\Rbar\\hspace{-.25ex}#1}}
\\catcode`\\†=\\active \\def †{{\\GreDagger}}
\\catcode`\\✠=\\active \\def ✠{{\\grecross}}
\\pagestyle{empty}
\\begin{document}
%s
\\end{document}
"""


def sha(code):
    """Returns sha1 hash of the code"""
    return sha1(code.encode(getfilesystemencoding())).hexdigest()


def latex(code):
    """LaTeX inline"""
    return RawInline('latex', code)


def latexblock(code):
    """LaTeX block"""
    return RawBlock('latex', code)


def htmlblock(code):
    """Html block"""
    return RawBlock('html', code)


def latexsnippet(code, kvs, staffsize=17, initiallines=1):
    """Take in account key/values"""
    snippet = ''
    staffsize = int(kvs['staffsize']) if 'staffsize' in kvs \
        else staffsize
    initiallines = int(kvs['initiallines']) if 'initiallines' in kvs \
        else initiallines
    annotationsize = .5 * staffsize
    if 'mode' in kvs:
        snippet = (
            "\\greannotation{{\\fontsize{%s}{%s}\\selectfont{}%s}}\n" %
            (annotationsize, annotationsize, kvs['mode'])
        ) + snippet
    if 'annotation' in kvs:
        snippet = (
            "\\grechangedim{annotationseparation}{%s mm}{fixed}\n"
            "\\greannotation{{\\fontsize{%s}{%s}\\selectfont{}%s}}\n" %
            (staffsize / 60, annotationsize, annotationsize, kvs['annotation'])
        ) + snippet
    snippet = (
        "\\gresetinitiallines{%s}\n" % initiallines +
        "\\grechangestaffsize{%s}\n" % staffsize +
        "\\grechangestyle{initial}{\\fontsize{%s}{%s}\\selectfont{}}" %
        (2.5 * staffsize, 2.5 * staffsize)
    ) + snippet
    snippet = "\\setlength{\\parskip}{0pt}\n" + snippet + code
    return snippet


def latex2png(snippet, outfile):
    """Compiles a LaTeX snippet to png"""
    pngimage = os.path.join(IMAGEDIR, outfile + '.png')
    texdocument = os.path.join(IMAGEDIR, 'tmp.tex')
    with open(texdocument, 'w') as doc:
        doc.write(LATEX_DOC % (snippet))
    environment = os.environ
    environment['shell_escape_commands'] = \
        "bibtex,bibtex8,kpsewhich,makeindex,mpost,repstopdf,\
        gregorio,gregorio-4_2_0"
    proc = Popen(
        ["lualatex", '-output-directory=' + IMAGEDIR, texdocument],
        stdin=PIPE,
        stdout=STDERR,
        env=environment
    )
    proc.communicate()
    proc.stdin.close()
    call(["pdfcrop", os.path.join(IMAGEDIR, "tmp.pdf")], stdout=STDERR)
    call(
        [
            "gs",
            "-sDEVICE=pngalpha",
            "-r144",
            "-sOutputFile=" + pngimage,
            os.path.join(IMAGEDIR, "tmp-crop.pdf"),
        ],
        stdout=STDERR,
    )


def png(contents, latex_command):
    """Creates a png if needed."""
    outfile = sha(contents + latex_command)
    src = os.path.join(IMAGEDIR, outfile + '.png')
    if not os.path.isfile(src):
        try:
            os.mkdir(IMAGEDIR)
            stderr.write('Created directory ' + IMAGEDIR + '\n')
        except OSError:
            pass
        latex2png(latex_command + "{" + contents + "}", outfile)
        stderr.write('Created image ' + src + '\n')
    return src


def properties(meta):
    try:
        staffsize = int(
            meta['music']['c']['gregorio']['c']['staffsize']['c']
        )
    except (KeyError, TypeError):
        staffsize = 17
    try:
        initiallines = int(
            meta['music']['c']['gregorio']['c']['initiallines']['c']
        )
    except (KeyError, TypeError):
        initiallines = 1
    return staffsize, initiallines


def gabc(key, value, fmt, meta):                   # pylint:disable=I0011,W0613
    """Handle gabc file inclusion and gabc code block."""
    if key == 'Code':
        [[ident, classes, kvs], contents] = value  # pylint:disable=I0011,W0612
        kvs = {key: value for key, value in kvs}
        if "gabc" in classes:
            staffsize, initiallines = properties(meta)
            if fmt == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return latex(
                    "\n\\smallskip\n{%\n" +
                    latexsnippet(
                        '\\gregorioscore{' + contents + '}',
                        kvs, staffsize, initiallines
                    ) +
                    "%\n}" +
                    label
                )
            else:
                infile = contents + (
                    '.gabc' if '.gabc' not in contents else ''
                )
                with open(infile, 'r') as doc:
                    code = doc.read().split('%%\n')[1]
                return [Image(['', [], []], [], [
                    png(
                        contents,
                        latexsnippet(
                            '\\gregorioscore', kvs, staffsize, initiallines
                        )
                    ),
                    ""
                ])]
    elif key == 'CodeBlock':
        [[ident, classes, kvs], contents] = value
        kvs = {key: value for key, value in kvs}
        if "gabc" in classes:
            staffsize, initiallines = properties(meta)
            if fmt == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return [latexblock(
                    "\n\\smallskip\n{%\n" +
                    latexsnippet(
                        '\\gabcsnippet{' + contents + '}',
                        kvs, staffsize, initiallines
                    ) +
                    "%\n}" +
                    label
                    )]
            else:
                return Para([Image(['', [], []], [], [
                    png(
                        contents,
                        latexsnippet(
                            '\\gabcsnippet', kvs, staffsize, initiallines
                        )
                    ),
                    ""
                ])])


if __name__ == "__main__":
    toJSONFilter(gabc)
