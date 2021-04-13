#!/usr/bin/python3

from panflute import (run_filters, Code, Header, Str, Para, Space,
RawInline, Plain)

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

def enumarate_exercise(elem, doc):
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
    '''
    if (type(elem) == Header and \
            len(elem.content) == 1 and \
            type(elem.content[0]) == Str and \
            elem.content[0].text == '[ej:]'
            ):
        if elem.level != 5:
            raise Exception()

        elem.content = [
                Str(text="Ej"),
                Space(),
                RawInline(text=r"\arabic{chapter}", format='tex'),
                Str(text="."),
                RawInline(text=r"\arabic{exercisecounter}", format='tex'),
                Str(text=":"),
        ]

        return [
                Plain(
                    RawInline(text=r"\stepcounter{exercisecounter}", format='tex')
                    ),
                elem,
                ]


def what(elem, doc):
    ''' Debugging / exploring / tracing. '''
    global trace_file
    print(type(elem), file=trace_file)
    if type(elem) == Header:
        print("-----", elem, "-----", file=trace_file)

    if type(elem) == Para:
        print(elem, file=trace_file)

if __name__ == '__main__':
    with open('output/logs/.pandoc_trace.log', 'wt') as f:
        trace_file = f
        run_filters([
            what,
            set_cpp_as_lang_for_inline_code,
            enumarate_exercise,
            ])