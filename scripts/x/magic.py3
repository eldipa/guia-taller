#!/usr/bin/env python3

from panflute import (run_filters, Code, Header, Str, Para, Space,
RawInline, Plain, Link, CodeBlock, RawBlock)

import sys, os

trace_file=None

def set_cpp_as_lang_for_inline_code(elem, doc):
    ''' Takes an inline code and mark it as C++ code if
        no other language was specified.

        This applies to only the Markdown text `foo` (backticks)
        if and only if no other class was set like in `bar`{.java}

        Example:
        In Markdown     -->    After filtering
        `char*`         -->    `char*`{.cpp}
        `bool`{.java}   -->    `bool`{.java}

    '''

    if type(elem) == Code and not elem.classes:
        elem.classes.append("cpp")


def kwargs_as_latex_options(kwargs):
    ret = []
    for key, value in kwargs.items():
        if isinstance(value, dict):
            value = kwargs_as_latex_options(value)
            value = '{' + value + '}'
        elif value == None or value == '':
            value = None
        elif isinstance(value, str):
            pass
        else:
            raise Exception()

        if value is None:
            ret.append(key)
        else:
            ret.append(f'{key}={value}')

    return ', '.join(ret)



from pygments.lexers import get_lexer_by_name

pygmented_block = r'''%s\begin{pygmented}[%s]%s%s%s\end{pygmented}%s'''
pygmented_inline = r'''\pyginline[%s]%s%s%s'''

def highlight_code_inline_and_blocks_with_pygments(elem, doc):
    if type(elem) in {CodeBlock, Code} and elem.classes:
        lexer = None
        lang, *flags = elem.classes[0].split(';')
        if lang == 'none':
            return # TODO

        try:
            lexer = get_lexer_by_name(lang)
        except:
            pass

        if not lexer:
            return

        code = elem.text

        # Options for "pygmentex"
        options = {
            'lang': lang,
            }

        # Options to make the box around the code invisible
        # and breakable (aka, that can span multiple pages)
        options.update({
            'boxrule': '0pt',
            'frame empty': None,
            'opacityback': '0',
            'opacityframe': '0',
            'breakable': None,
            })

        # Options to align the code: left and top (reasonable)
        options.update({
            'halign': 'left',
            'valign': 'top',
            })

        # Options to style source code: candombe style and minimal size.
        # The candombe style is defined in scripts/x/pygmentex.py
        options.update({
            'size': 'minimal',
            'sty': 'candombe',
            })

        flags = set(filter(None, flags))
        if 'frameleft' in flags:
            # If the user wants a "frameleft" we want to show the box
            # but only the left line which will look like a ruler.
            flags.discard('frameleft')
            options.pop('frame empty')
            options.update({
                'frame hidden': None,
                'enhanced jigsaw': None,
                'opacityframe': '1',
                'boxrule': '2px',
                'colframe': 'black',
                'borderline west': '{0.5pt}{-1.5pt}{black}'
                })

        if 'diagram' in flags:
            flags.discard('diagram')

            # make the code unbreakable (make it a single piece
            # that cannot spawn multiple pages)
            options.pop('breakable')

            # try to estimate the width of the diagram based on the
            # maximum line length, assuming that a full line is made of
            # 70 characters
            estimated_linewidth_in_chars = 70
            width_ratio = max((len(line) for line in code.split('\n'))) / estimated_linewidth_in_chars

            # ratios close to 1 (or above) should be mapped to a full
            # line width (no ratio)
            width_ratio = min(width_ratio, 0.99)
            if width_ratio < 0.98:
                width_ratio = f'{width_ratio:.2f}'
            else:
                width_ratio = ''

            # make the diagram
            # to be centered on the page
            options.update({
                'center': None,
                'width': r'%s\linewidth' % width_ratio, # TODO
                })

            # see pygmentex script
            if 'nostyle' in flags:
                flags.discard('nostyle')
                options['sty'] = 'nostylediagram'
            else:
                options['sty'] = 'candombediagram'


        attrs = kwargs_as_latex_options(options)
        if flags:
            attrs += ', ' + ', '.join(flags)

        if type(elem) == Code:
            # pick a valid separator that is not present in the code
            # that we want to wrap
            for delim in ('|', '!', '@'):
                if delim not in elem.text:
                    break
            else:
                raise Exception("We don't know which separator to use.")

            text = pygmented_inline % (attrs, delim, code, delim)
            return RawInline(text=text, format='tex')
        elif type(elem) == CodeBlock:
            pre = r'\disablehyphenation' + '\n'
            pos = '\n' + r'\enablehyphenation'
            text = pygmented_block % (pre, attrs, '\n', code, '\n', pos)
            return RawBlock(text=text, format='tex')
        else:
            assert False

def cpp_pretty_typing(elem, doc):
    ''' Replace C++ and C/C++ strings with some latex code
        to type them prettier. '''
    global trace_file
    if type(elem) in {Str} and 'C++' in elem.text:
        if 'C/C++' in elem.text:
            token = 'C/C++'
            latex = r'\Ccplusplus{}'
        else:
            token = 'C++'
            latex = r'\cplusplus{}'

        left, right = elem.text.split(token)
        return [Str(left), RawInline(text=latex, format='tex'), Str(right)]


def what(elem, doc):
    ''' Debugging / exploring / tracing. '''
    global trace_file
    if trace_file is None:
        fname = os.getenv("PANFLUTE_TRACE_FILENAME", 'unknown.panflute-trace')
        trace_file = open(fname, 'wt')

    print(type(elem), file=trace_file)
    if type(elem) in {CodeBlock, Code}:
        print("-----", elem, "-----", file=trace_file)
        print(dir(elem), elem.attributes, file=trace_file)

    #if type(elem) == Link:
    #    print(elem, file=trace_file)

if __name__ == '__main__':
    try:
        run_filters([
            what,
            set_cpp_as_lang_for_inline_code,
            highlight_code_inline_and_blocks_with_pygments,
            cpp_pretty_typing,
            ])
    finally:
        if trace_file is not None:
            trace_file.close()
