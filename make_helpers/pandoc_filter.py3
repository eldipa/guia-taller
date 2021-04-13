#!/usr/bin/python3

from panflute import run_filters, Code, Header, Str, Para, Space, RawInline

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
    ''' Replace the literal string '[ej:]' with 'Ej x.y:' where
        'x' is replaced by the current chapter number and 'y' is
        the incremented 'exercisecounter' value.

        The 'exercisecounter' is incremented before getting the value
        so 'exercisecounter' should be initialized with zero to make
        sense.

        Example:
        In Markdown
        [ej:] Resolve the following equation

        In pseudo-Latex
        (++exercisecounter)
        Ej (chapter).(exercisecounter):
    '''
    if type(elem) == Str and elem.text == '[ej:]':
        return [
            Str(text="Ej"),
            Space(),
            RawInline(text=r"\stepcounter{exercisecounter}", format='tex'),
            RawInline(text=r"\arabic{chapter}", format='tex'),
            Str(text="."),
            RawInline(text=r"\arabic{exercisecounter}", format='tex'),
            Str(text=":"),
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
            set_cpp_as_lang_for_inline_code,
            enumarate_exercise,
            what
            ])
