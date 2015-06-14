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


IMAGEDIR = "tmp_gabc"
LATEX_DOC = """\\documentclass{article}
\\usepackage{libertine}
\\usepackage[autocompile]{gregoriotex}
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


def latex2png(snippet, outfile):
    """Compiles a LaTeX snippet to png"""
    pngimage = os.path.join(IMAGEDIR, outfile + '.png')
    environment = os.environ
    environment['openout_any'] = 'a'
    environment['shell_escape_commands'] = \
        "bibtex,bibtex8,kpsewhich,makeindex,mpost,repstopdf,gregorio"
    proc = Popen(
        ["lualatex", '-output-directory=' + IMAGEDIR],
        stdin=PIPE,
        stdout=DEVNULL,
        env=environment
    )
    proc.stdin.write(
        (
            LATEX_DOC % (snippet)
        ).encode("utf-8")
    )
    proc.communicate()
    proc.stdin.close()
    call(["pdfcrop", os.path.join(IMAGEDIR, "texput.pdf")], stdout=DEVNULL)
    call(
        [
            "gs",
            "-sDEVICE=pngalpha",
            "-r144",
            "-sOutputFile=" + pngimage,
            os.path.join(IMAGEDIR, "texput-crop.pdf"),
        ],
        stdout=DEVNULL,
    )


def png(contents, outfile, latex_command):
    """Creates a png if needed."""
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


def gabc(key, value, fmt, meta):                   # pylint:disable=I0011,W0613
    """Handle gabc file inclusion and gabc code block."""
    if key == 'Code':
        [[ident, classes, kvs], contents] = value  # pylint:disable=I0011,W0612
        if "gabc" in classes:
            if fmt == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return latex('\\includescore{' + contents + '}' + label)
            else:
                infile = contents + (
                    '.gabc' if '.gabc' not in contents else ''
                )
                with open(infile, 'r') as doc:
                    code = doc.read().split('%%\n')[1]
                outfile = sha(code)
                return [
                    Image([], [png(contents, outfile, '\\includescore'), ""])
                ]
    elif key == 'CodeBlock':
        [[ident, classes, kvs], contents] = value
        if "gabc" in classes:
            if fmt == "latex":
                if ident == "":
                    label = ""
                else:
                    label = '\\label{' + ident + '}'
                return [latexblock('\\gabcsnippet{' + contents + '}' + label)]
            else:
                outfile = sha(contents)
                return Para(
                    [Image([], [png(contents, outfile, '\\gabcsnippet'), ""])]
                )


if __name__ == "__main__":
    toJSONFilter(gabc)
