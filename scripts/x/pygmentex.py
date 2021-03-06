#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    PygmenTeX
    ~~~~~~~~~

    PygmenTeX is a converter that do syntax highlighting of snippets of
    source code extracted from a LaTeX file.

    :copyright: Copyright 2020 by José Romildo Malaquias
    :license: BSD, see LICENSE for details
"""

__version__ = '0.10'
__docformat__ = 'restructuredtext'

import sys
import getopt
import re
from os.path import splitext

from pygments import highlight
from pygments.styles import get_style_by_name
from pygments.lexers import get_lexer_by_name
from pygments.formatters.latex import LatexFormatter, escape_tex, _get_ttype_name
from pygments.util import get_bool_opt, get_int_opt
from pygments.lexer import Lexer
from pygments.token import Token
from pygments.util import guess_decode


# ----------------------
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal

class CandombeStyle(Style):
    # a slighted tweaked version of Pygments' Tango style

    background_color = "#f8f8f8"
    default_style = ""

    styles = {
        # No corresponding class for the following:
        #Text:                     "", # class:  ''
        #Error:                     "#a40000 border:#ef2929", # class: 'err'
        #Whitespace:                "underline #f8f8f8",      # class: 'w'
        Whitespace:                "#f8f8f8",      # class: 'w'
        Other:                     "#000000",                # class 'x'

        Comment:                   "italic #8f5902", # class: 'c'
        Comment.Multiline:         "italic #8f5902", # class: 'cm'
        Comment.Preproc:           "italic #8f5902", # class: 'cp'
        Comment.Single:            "italic #8f5902", # class: 'c1'
        Comment.Special:           "italic #8f5902", # class: 'cs'

        Keyword:                   "bold #204a87",   # class: 'k'
        Keyword.Constant:          "bold #204a87",   # class: 'kc'
        Keyword.Declaration:       "bold #204a87",   # class: 'kd'
        Keyword.Namespace:         "bold #204a87",   # class: 'kn'
        Keyword.Pseudo:            "bold #204a87",   # class: 'kp'
        Keyword.Reserved:          "bold #204a87",   # class: 'kr'
        Keyword.Type:              "bold #204a87",   # class: 'kt'

        Operator:                  "bold #ce5c00",   # class: 'o'
        Operator.Word:             "bold #204a87",   # class: 'ow' - like keywords

        Punctuation:               "bold #000000",   # class: 'p'

        # because special names such as Name.Class, Name.Function, etc.
        # are not recognized as such later in the parsing, we choose them
        # to look the same as ordinary variables.
        Name:                      "#000000",        # class: 'n'
        Name.Attribute:            "#c4a000",        # class: 'na' - to be revised
        Name.Builtin:              "#204a87",        # class: 'nb'
        Name.Builtin.Pseudo:       "#3465a4",        # class: 'bp'
        Name.Class:                "#000000",        # class: 'nc' - to be revised
        Name.Constant:             "#000000",        # class: 'no' - to be revised
        Name.Decorator:            "bold #5c35cc",   # class: 'nd' - to be revised
        Name.Entity:               "#ce5c00",        # class: 'ni'
        Name.Exception:            "bold #cc0000",   # class: 'ne'
        Name.Function:             "#000000",        # class: 'nf'
        Name.Property:             "#000000",        # class: 'py'
        Name.Label:                "#f57900",        # class: 'nl'
        Name.Namespace:            "#000000",        # class: 'nn' - to be revised
        Name.Other:                "#000000",        # class: 'nx'
        Name.Tag:                  "bold #204a87",   # class: 'nt' - like a keyword
        Name.Variable:             "#000000",        # class: 'nv' - to be revised
        Name.Variable.Class:       "#000000",        # class: 'vc' - to be revised
        Name.Variable.Global:      "#000000",        # class: 'vg' - to be revised
        Name.Variable.Instance:    "#000000",        # class: 'vi' - to be revised

        # since the tango light blue does not show up well in text, we choose
        # a pure blue instead.
        Number:                    "bold #aa22ff",   # class: 'm'
        Number.Float:              "bold #aa22ff",   # class: 'mf'
        Number.Hex:                "bold #aa22ff",   # class: 'mh'
        Number.Integer:            "bold #aa22ff",   # class: 'mi'
        Number.Integer.Long:       "bold #aa22ff",   # class: 'il'
        Number.Oct:                "bold #aa22ff",   # class: 'mo'

        Literal:                   "#000000",        # class: 'l'
        Literal.Date:              "#000000",        # class: 'ld'

        String:                    "#4e9a06",        # class: 's'
        String.Backtick:           "#4e9a06",        # class: 'sb'
        String.Char:               "#4e9a06",        # class: 'sc'
        String.Doc:                "italic #8f5902", # class: 'sd' - like a comment
        String.Double:             "#4e9a06",        # class: 's2'
        String.Escape:             "#4e9a06",        # class: 'se'
        String.Heredoc:            "#4e9a06",        # class: 'sh'
        String.Interpol:           "#4e9a06",        # class: 'si'
        String.Other:              "#4e9a06",        # class: 'sx'
        String.Regex:              "#4e9a06",        # class: 'sr'
        String.Single:             "#4e9a06",        # class: 's1'
        String.Symbol:             "#4e9a06",        # class: 'ss'

        Generic:                   "#000000",        # class: 'g'
        Generic.Deleted:           "#a40000",        # class: 'gd'
        Generic.Emph:              "italic #000000", # class: 'ge'
        Generic.Error:             "#ef2929",        # class: 'gr'
        Generic.Heading:           "bold #000080",   # class: 'gh'
        Generic.Inserted:          "#00A000",        # class: 'gi'
        Generic.Output:            "italic #000000", # class: 'go'
        Generic.Prompt:            "#8f5902",        # class: 'gp'
        Generic.Strong:            "bold #000000",   # class: 'gs'
        Generic.Subheading:        "bold #800080",   # class: 'gu'
        Generic.Traceback:         "bold #a40000",   # class: 'gt'
    }

class NoStyle(Style):
    background_color = "#f8f8f8"
    default_style = ""

    styles = {k: '#000000' for k in CandombeStyle.styles.keys()}

# --------------------------

###################################################
# The following code is in >=pygments-2.0
###################################################
class EnhancedLatexFormatter(LatexFormatter):
    r"""
    This is an enhanced LaTeX formatter.
    """
    name = 'EnhancedLaTeX'
    aliases = []

    def __init__(self, **options):
        LatexFormatter.__init__(self, **options)
        self.escapeinside = options.get('escapeinside', '')
        if len(self.escapeinside) == 2:
            self.left = self.escapeinside[0]
            self.right = self.escapeinside[1]
        else:
            self.escapeinside = ''

    def format_unencoded(self, tokensource, outfile):
        # TODO: add support for background colors
        t2n = self.ttype2name
        cp = self.commandprefix

        if self.full:
            realoutfile = outfile
            outfile = StringIO()

        outfile.write(r'\begin{Verbatim}[commandchars=\\\{\}')
        if self.linenos:
            start, step = self.linenostart, self.linenostep
            outfile.write(',numbers=left' +
                          (start and ',firstnumber=%d' % start or '') +
                          (step and ',stepnumber=%d' % step or ''))
        if self.mathescape or self.texcomments or self.escapeinside:
            outfile.write(r',codes={\catcode`\$=3\catcode`\^=7\catcode`\_=8}')
        if self.verboptions:
            outfile.write(',' + self.verboptions)
        outfile.write(']\n')

        for ttype, value in tokensource:
            if ttype in Token.Comment:
                if self.texcomments:
                    # Try to guess comment starting lexeme and escape it ...
                    start = value[0:1]
                    for i in range(1, len(value)):
                        if start[0] != value[i]:
                            break
                        start += value[i]

                    value = value[len(start):]
                    start = escape_tex(start, self.commandprefix)

                    # ... but do not escape inside comment.
                    value = start + value
                elif self.mathescape:
                    # Only escape parts not inside a math environment.
                    parts = value.split('$')
                    in_math = False
                    for i, part in enumerate(parts):
                        if not in_math:
                            parts[i] = escape_tex(part, self.commandprefix)
                        in_math = not in_math
                    value = '$'.join(parts)
                elif self.escapeinside:
                    text = value
                    value = ''
                    while len(text) > 0:
                        a,sep1,text = text.partition(self.left)
                        if len(sep1) > 0:
                            b,sep2,text = text.partition(self.right)
                            if len(sep2) > 0:
                                value += escape_tex(a, self.commandprefix) + b
                            else:
                                value += escape_tex(a + sep1 + b, self.commandprefix)
                        else:
                            value = value + escape_tex(a, self.commandprefix)
                else:
                    value = escape_tex(value, self.commandprefix)
            elif ttype not in Token.Escape:
                value = escape_tex(value, self.commandprefix)
            styles = []
            while ttype is not Token:
                try:
                    styles.append(t2n[ttype])
                except KeyError:
                    # not in current style
                    styles.append(_get_ttype_name(ttype))
                ttype = ttype.parent
            styleval = '+'.join(reversed(styles))
            if styleval:
                spl = value.split('\n')
                for line in spl[:-1]:
                    if line:
                        outfile.write("\\%s{%s}{%s}" % (cp, styleval, line))
                    outfile.write('\n')
                if spl[-1]:
                    outfile.write("\\%s{%s}{%s}" % (cp, styleval, spl[-1]))
            else:
                outfile.write(value)

        outfile.write('\\end{Verbatim}\n')

        if self.full:
            realoutfile.write(DOC_TEMPLATE %
                dict(docclass  = self.docclass,
                     preamble  = self.preamble,
                     title     = self.title,
                     encoding  = self.encoding or 'latin1',
                     styledefs = self.get_style_defs(),
                     code      = outfile.getvalue()))

class LatexEmbeddedLexer(Lexer):
    r"""

    This lexer takes one lexer as argument, the lexer for the language
    being formatted, and the left and right delimiters for escaped text.

    First everything is scanned using the language lexer to obtain
    strings and comments. All other consecutive tokens are merged and
    the resulting text is scanned for escaped segments, which are given
    the Token.Escape type. Finally text that is not escaped is scanned
    again with the language lexer.
    """
    def __init__(self, left, right, lang, **options):
        self.left = left
        self.right = right
        self.lang = lang
        Lexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        buf = ''
        for i, t, v in self.lang.get_tokens_unprocessed(text):
            if t in Token.Comment or t in Token.String:
                if buf:
                    for x in self.get_tokens_aux(idx, buf):
                        yield x
                    buf = ''
                yield i, t, v
            else:
                if not buf:
                    idx = i
                buf += v
        if buf:
            for x in self.get_tokens_aux(idx, buf):
                yield x

    def get_tokens_aux(self, index, text):
        while text:
            a, sep1, text = text.partition(self.left)
            if a:
                for i, t, v in self.lang.get_tokens_unprocessed(a):
                    yield index + i, t, v
                    index += len(a)
            if sep1:
                b, sep2, text = text.partition(self.right)
                if sep2:
                    yield index + len(sep1), Token.Escape, b
                    index += len(sep1) + len(b) + len(sep2)
                else:
                    yield index, Token.Error, sep1
                    index += len(sep1)
                    text = b
###################################################

GENERIC_DEFINITIONS_1 = r'''% -*- mode: latex -*-

\makeatletter

\newdimen\LineNumberWidth
'''

GENERIC_DEFINITIONS_2 = r'''
\makeatother
'''


INLINE_SNIPPET_TEMPLATE = r'''
\expandafter\def\csname pygmented@snippet@%(number)s\endcsname{%%
  \pygmented@snippet@inlined{%%
%(body)s%%
}}
'''

DISPLAY_SNIPPET_TEMPLATE = r'''
\expandafter\def\csname pygmented@snippet@%(number)s\endcsname{%%
  \begin{pygmented@snippet@framed}%%
%(body)s%%
  \end{pygmented@snippet@framed}%%
}
'''

DISPLAY_LINENOS_SNIPPET_TEMPLATE = r'''
\expandafter\def\csname pygmented@snippet@%(number)s\endcsname{%%
  \begingroup
    \def\pygmented@alllinenos{(%(linenumbers)s)}%%
    \begin{pygmented@snippet@framed}%%
%(body)s%%
    \end{pygmented@snippet@framed}%%
  \endgroup
}
'''


def pyg(outfile, outencoding, n, opts, extra_opts, text, usedstyles, inline_delim = ''):
    try:
        lexer = get_lexer_by_name(opts['lang'])
    except ClassNotFound as err:
        sys.stderr.write('Error: ')
        sys.stderr.write(str(err))
        return ""

    # global _fmter
    _fmter = EnhancedLatexFormatter()

    escapeinside = opts.get('escapeinside', '')
    if len(escapeinside) == 2:
        left = escapeinside[0]
        right = escapeinside[1]
        _fmter.escapeinside = escapeinside
        _fmter.left = left
        _fmter.right = right
        lexer = LatexEmbeddedLexer(left, right, lexer)

    gobble = abs(get_int_opt(opts, 'gobble', 0))
    if gobble:
        lexer.add_filter('gobble', n=gobble)

    tabsize = abs(get_int_opt(opts, 'tabsize', 0))
    if tabsize:
        lexer.tabsize = tabsize

    lexer.encoding = ''
    # _fmter.encoding = outencoding

    stylename = opts['sty']

    honorspacewidth = False
    if stylename in ('candombe', 'candombefix', 'candombediagram', 'nostylediagram'):
        _fmter.style = NoStyle if stylename == 'nostylediagram' else CandombeStyle
        honorspacewidth = stylename in ('candombefix', 'candombediagram', 'nostylediagram')
    else:
        _fmter.style = get_style_by_name(stylename)

    _fmter._create_stylesheet()

    _fmter.texcomments = get_bool_opt(opts, 'texcomments', False)
    _fmter.mathescape = get_bool_opt(opts, 'mathescape', False)


    if stylename not in usedstyles:
        styledefs = _fmter.get_style_defs() \
            .replace('#', '##') \
            .replace(r'\##', r'\#') \
            .replace(r'\makeatletter', '') \
            .replace(r'\makeatother', '') \
            .replace('\n', '%\n')
        outfile.write(
            '\\def\\PYstyle{0}{{%\n{1}%\n}}%\n'.format(stylename, styledefs))
        usedstyles.append(stylename)

    x = highlight(text, lexer, _fmter)

    m = re.match(r'\\begin\{Verbatim}(.*)\n([\s\S]*?)\n\\end\{Verbatim}(\s*)\Z',
                 x)
    if m:
        linenos = get_bool_opt(opts, 'linenos', False)
        linenostart = abs(get_int_opt(opts, 'linenostart', 1))
        linenostep = abs(get_int_opt(opts, 'linenostep', 1))
        lines0 = m.group(2).split('\n')
        numbers = []
        lines = []
        counter = linenostart
        for line in lines0:
            line = re.sub(r'^ ', r'\\makebox[0pt]{\\phantom{Xy}} ', line)
            line = re.sub(r' ', '~', line)
            if linenos:
                if (counter - linenostart) % linenostep == 0:
                    line = r'\pygmented@lineno@do{' + str(counter) + '}' + line
                    numbers.append(str(counter))
                counter = counter + 1
            lines.append(line)
        if inline_delim:
            outfile.write(INLINE_SNIPPET_TEMPLATE %
                dict(number    = n,
                     style     = stylename,
                     options   = extra_opts,
                     body      = '\\newline\n'.join(lines)))
        else:
            if linenos:
                template = DISPLAY_LINENOS_SNIPPET_TEMPLATE
            else:
                template = DISPLAY_SNIPPET_TEMPLATE

            # The '~' is a special Latex character that means an
            # unbreakable space and it is used by Pygments to type the
            # spaces.
            # Unfortunately the width of each space character is smaller
            # than the size of the rest of the characters and while it
            # is ok for normal source code, it is not ok when doing an
            # ASCII diagram
            #
            # The fix is to replace all the ~ by a horizontal phantom
            # space which width will be the same of the width of the
            # given character (in this case a 'm').
            #
            # This should be safe even if the source code has a ~
            # because Pygments will replace them with \PYZti{} before
            # so we should be replacing only the ~ that represent
            # spaces.
            #
            # https://github.com/pygments/pygments/blob/master/pygments/formatters/latex.py
            # https://tex.stackexchange.com/questions/74353/what-commands-are-there-for-horizontal-spacing
            if honorspacewidth:
                lines = [l.replace('~',r'\hphantom{m}') for l in lines]

            outfile.write(template %
                dict(number      = n,
                     style       = stylename,
                     options     = extra_opts,
                     linenosep   = opts['linenosep'],
                     linenumbers = ','.join(numbers),
                     body        = '\\newline\n'.join(lines)))



def parse_opts(basedic, opts):
    dic = basedic.copy()
    for opt in re.split(r'\s*,\s*', opts):
        x = re.split(r'\s*=\s*', opt)
        if len(x) == 2 and x[0] and x[1]:
            dic[x[0]] = x[1]
        elif len(x) == 1 and x[0]:
            dic[x[0]] = True
    return dic



_re_display = re.compile(
    r'^<@@pygmented@display@(\d+)\n(.*)\n([\s\S]*?)\n>@@pygmented@display@\1$',
    re.MULTILINE)

_re_inline = re.compile(
    r'^<@@pygmented@inline@(\d+)\n(.*)\n([\s\S]*?)\n>@@pygmented@inline@\1$',
    re.MULTILINE)

_re_input = re.compile(
    r'^<@@pygmented@input@(\d+)\n(.*)\n([\s\S]*?)\n>@@pygmented@input@\1$',
    re.MULTILINE)

def convert(code, outfile, outencoding):
    """
    Convert ``code``
    """
    outfile.write(GENERIC_DEFINITIONS_1)

    opts = { 'lang'      : 'c',
             'sty'       : 'default',
             'linenosep' : '0pt',
             'tabsize'   : '8',
             'encoding'  : 'guess',
           }

    usedstyles = [ ]
    styledefs = ''

    pos = 0

    while pos < len(code):
        if code[pos].isspace():
            pos = pos + 1
            continue

        m = _re_inline.match(code, pos)
        if m:
            pyg(outfile,
                outencoding,
                m.group(1),
                parse_opts(opts.copy(), m.group(2)),
                '',
                m.group(3),
                usedstyles,
                True)
            pos = m.end()
            continue

        m = _re_display.match(code, pos)
        if m:
            pyg(outfile,
                outencoding,
                m.group(1),
                parse_opts(opts.copy(), m.group(2)),
                '',
                m.group(3),
                usedstyles)
            pos = m.end()
            continue

        m = _re_input.match(code, pos)
        if m:
            opts_new = parse_opts(opts, m.group(2))
            try:
                filecontents, inencoding = read_input(m.group(3), opts_new['encoding'])
            except Exception as err:
                print('Error: cannot read input file: ', err, file=sys.stderr)
            else:
                pyg(outfile,
                    outencoding,
                    m.group(1),
                    opts_new,
                    "",
                    filecontents,
                    usedstyles)
            pos = m.end()
            continue

        sys.stderr.write('Error: invalid input file contents: ignoring')
        break

    outfile.write(GENERIC_DEFINITIONS_2)

def read_input(filename, encoding):
    with open(filename, 'rb') as infp:
        code = infp.read()

    if not encoding or encoding == 'guess':
        code, encoding = guess_decode(code)
    else:
        code = code.decode(encoding)

    return code, encoding


USAGE = """\
Usage: %s [-o <output file name>] <input file name>
       %s -h | -V

The input file should consist of a sequence of source code snippets, as
produced by the `pygmentex` LaTeX package. Each code snippet is
highlighted using Pygments, and a LaTeX command that expands to the
highlighted code snippet is written to the output file.

It also writes to the output file a set of LaTeX macro definitions the
Pygments styles that are used in the code snippets.

If no output file name is given, use `<input file name>.pygmented`.

The -e option enables escaping to LaTex. Text delimited by the <left>
and <right> characters is read as LaTeX code and typeset accordingly. It
has no effect in string literals. It has no effect in comments if
`texcomments` or `mathescape` is set.

The -h option prints this help.

The -V option prints the package version.
"""


def main(args = sys.argv):
    """
    Main command line entry point.
    """
    usage = USAGE % ((args[0],) * 2)

    try:
        popts, args = getopt.getopt(args[1:], 'e:o:hV')
    except getopt.GetoptError as err:
        sys.stderr.write(usage)
        return 2
    opts = {}
    for opt, arg in popts:
        opts[opt] = arg

    if not opts and not args:
        print(usage)
        return 0

    if opts.pop('-h', None) is not None:
        print(usage)
        return 0

    if opts.pop('-V', None) is not None:
        print('PygmenTeX version %s, (c) 2020 by José Romildo.' % __version__)
        return 0
 
    if len(args) != 1:
        sys.stderr.write(usage)
        return 2
    infn = args[0]
    try:
        code, inencoding = read_input(infn, "guess")
    except Exception as err:
        print('Error: cannot read input file: ', err, file=sys.stderr)
        return 1

    outfn = opts.pop('-o', None)
    if not outfn:
        root, ext = splitext(infn)
        outfn = root + '.pygmented'
    try:
        outfile = open(outfn, 'w')
    except Exception as err:
        print('Error: cannot open output file: ', err, file=sys.stderr)
        return 1

    convert(code, outfile, inencoding)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(1)
