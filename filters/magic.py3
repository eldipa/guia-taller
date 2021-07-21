#!/usr/bin/env python3

from panflute import (run_filters, Code, Header, Str, Para, Space,
RawInline, Plain, Link, CodeBlock, RawBlock)

import sys

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

def XXwarn_about_unprotect_underscore_in_link_recursive(elem):
    if type(elem) == Code and '_' in elem.text:
        print(f"ERR: a code inside of a href/link cannot have an 'underscore' -> {elem}", file=sys.stderr)

def XXwarn_about_unprotect_underscore_in_link(elem, doc):
    if type(elem) == Link:
        for el in elem.content:
            warn_about_unprotect_underscore_in_link_recursive(el)

def NOT_USED_enumarate_exercises_and_projects(elem, doc):
    ''' Replace the header with a literal string '[ej:]' with 'Ej x.y:' where
        'x' is replaced by the current chapter number and 'y' is
        the incremented 'exercisecounter' value.

        The 'exercisecounter' is incremented before getting the value
        so 'exercisecounter' should be initialized with zero to make
        sense.

        Example:
        In Markdown
        ##### [ej:]
        Resolve the following equation

        In pseudo-Latex
        (++exercisecounter)
        ##### Ej (chapter).(exercisecounter):
        Resolve the following equation

        Note: only headers of level 5 are allowed. Other header with the
        same literal string will be considered an error.

        Do the same replacements for headers with '[proj:]' using a
        different counter: 'projectcounter'.
    '''
    if (type(elem) == Header and \
            len(elem.content) >= 1 and \
            type(elem.content[0]) == Str
            ):

        first = elem.content[0].text
        if not first.startswith('[ej:') and not first.startswith('[proj:'):
            return

        if first not in ('[ej:]', '[proj:]', '[proj:'):
            raise Exception()

        if elem.level != 5:
            raise Exception()

        # so far, the header must be one of:
        #   [ej:]
        #   [proj:]
        #   [proj: xxx]
        #   [proj: xxx ]

        is_exercise = first == '[ej:]'
        del first

        if is_exercise and len(elem.content) != 1:
            raise Exception()

        if is_exercise:
            label = "Ej"
            counter = "exercisecounter"
            title = []
        else:
            label = "Proj"
            counter = "projectcounter"

            if len(elem.content) == 1:
                # just nameless [proj:]
                title = []
            else:
                # strip head '[proj:'
                del elem.content[0]

                # ensure that the last item is 'xxx]'
                last = elem.content[-1]
                if not type(last) == Str:
                    raise Exception()

                if not last.text.endswith(']') or len(last.text) <= 1:
                    raise Exception()

                # strip the trailing ']'
                if len(last.text) == 1:
                    del elem.content[-1]
                else:
                    last.text = last.text[:-1]

                title = list(elem.content)

        elem.content = [
                Str(text=label),
                Space(),
                RawInline(text=r"\arabic{chapter}", format='tex'),
                Str(text="."),
                RawInline(text=r"\arabic{%s}" % counter, format='tex'),
                *title,
                Str(text=':')

        ]

        return [
                Plain(
                    RawInline(text=r"\stepcounter{%s}" % counter, format='tex')
                    ),
                elem,
                ]

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


def str_options_as_dict(s, sep=';'):
    pass


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

        options = {
            'lang': lang,
            'boxrule': '0pt',
            'frame empty': None,
            'opacityback': '0',
            'opacityframe': '0',
            'halign': 'left',
            'valign': 'top',
            'size': 'minimal',
            'sty': 'candombe',
            }

        flags = set(filter(None, flags))
        if 'frameleft' in flags:
            flags.discard('frameleft')
            options.pop('frame empty')
            options.update({
                'frame hidden': None,
                'enhanced': None,
                'opacityframe': '1',
                'boxrule': '2px',
                'colframe': 'black',
                'borderline west': '{0.5pt}{-1.5pt}{black}'
                })

        attrs = ', ' + kwargs_as_latex_options(options)
        if flags:
            attrs += ', ' + ', '.join(flags)

        code = elem.text

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

def what(elem, doc):
    ''' Debugging / exploring / tracing. '''
    global trace_file
    print(type(elem), file=trace_file)
    if type(elem) in {CodeBlock, Code}:
        print("-----", elem, "-----", file=trace_file)
        print(dir(elem), elem.attributes, file=trace_file)

    #if type(elem) == Link:
    #    print(elem, file=trace_file)

if __name__ == '__main__':
    fname = '/dev/null'
    #fname = 'log.log'
    with open(fname, 'wt') as f:
        trace_file = f
        run_filters([
            what,
            set_cpp_as_lang_for_inline_code,
            highlight_code_inline_and_blocks_with_pygments,
            ])
