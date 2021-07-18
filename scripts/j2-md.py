
# See https://github.com/kolypto/j2cli
# pip install j2cli

import jinja2

@jinja2.contextfunction
def include_file_raw(ctx, name, indent=0):
    ''' Function to open and read the given file (<name>) and
        return its content as-is (raw). Jinja will not try to
        parse it in any way.

        This contrast with Jinja's include tag ({% include fname %})
        which process the file as a Jinja template before returning
        it.

        If <indent> is given, indent all the lines by that amound of
        spaces even if the lines that are empty. (Useful to use
        in a YAML file where the file uses the indentation as part
        of the format, similar to Python).

        Example:

            {{ include_file_raw(src_dir + "/" + fname) }}
    '''
    env = ctx.environment
    content = env.loader.get_source(env, name)[0]

    if indent:
        # Note: Python's textwrap.indent is too smart for this
        indent = ' ' * indent
        content = '\n'.join(indent + line for line in content.split('\n'))
    return jinja2.Markup(content)


def as_markup_latex(tex):
    return jinja2.Markup('```{=latex}\n%s\n```' % tex)

exercise_or_project_marker = r'''\stepcounter{%(countername)s} \subsubsection{%(prefix)s \arabic{chapter}.\arabic{%(countername)s}: %(title)s}'''

@jinja2.contextfunction
def exercise_marker(ctx):
    content = exercise_or_project_marker % dict(prefix='Ej', countername='exercisecounter', title='')
    return as_markup_latex(content)


@jinja2.contextfunction
def project_marker(ctx, title=''):
    content = exercise_or_project_marker % dict(prefix='Proj', countername='projectcounter', title=title)
    return as_markup_latex(content)

def strip_fenced_code_block_markers(src):
    lines = src.strip().split('\n')
    if len(lines) <= 2 or not lines[0].startswith('```') or not lines[-1].startswith('```'):
        raise Exception("Expected a Fenced-Code Block.")

    # ensamble the source again
    return '\n'.join(lines[1:-1])

import dot2tex

@jinja2.contextfunction
def diagram_graphviz(ctx, src, **kargs):
    ''' Take a dot graph and recoded as a tikz graph.

        Source should be a graph wrapped in a fenced-code block:

        src == """
            ```foo
            digraph G {
                a_1-> a_2 -> a_3 -> a_1;
            }
            ```
            """

        Return a Latex literal. Arguments are passed to dot2tex.
    '''
    src = strip_fenced_code_block_markers(src)

    # Ensure that codeonly or figonly is True. The former
    # generates Tikz code without an environment (so we could keep
    # adding Tikz code) and the latter includes the environment.
    # One of them must be set otherwise dot2tex will generate
    # a full Tex document.
    if not kargs.get('codeonly', False):
        kargs['figonly'] = True
    tex = dot2tex.dot2tex(src, **kargs)
    return as_markup_latex(tex)

@jinja2.contextfunction
def figure_fig(ctx, path, position='here', caption='', captionpos='bottom',
        figparams={}, wrapsize=r'0.25\textwidth'):
    ''' Take a dot graph and recoded as a tikz graph.

        Source should be a graph wrapped in a fenced-code block:

        src == """
            ```foo
            digraph G {
                a_1-> a_2 -> a_3 -> a_1;
            }
            ```
            """

        Return a Latex literal. Arguments are passed to dot2tex.
    '''
    # Build the "include the figure" tex code
    figparams_str = ','.join(f'{key}={val}' for key, val in figparams.items())
    fig_include_tex = r'\includegraphics[%s]{%s}' % (figparams_str, path)

    # Process the caption, if any
    caption = caption.strip()

    # Center the image and put a caption if any.
    assert captionpos in ('top', 'bottom')
    if not caption:
        env_content_tex = r'''
\centering
%s
''' % (fig_include_tex)
    elif captionpos == 'top':
        env_content_tex = r'''
\centering
\caption{%s}
%s
''' % (caption, fig_include_tex)
    elif captionpos == 'bottom':
        env_content_tex = r'''
\centering
%s
\caption{%s}
''' % (fig_include_tex, caption)
    else:
        assert False

    # Remove trailing space
    env_content_tex = env_content_tex.strip()

    # Choose the environment based on the position of the figure
    # and configure it
    assert position in (
            'top', 'bottom', 'page', 'here', 'left', 'right',
            'inner', 'outer')

    position_flag = position[0]
    if position in ('left', 'right', 'inner', 'outer'):
        fig_env_tex = r'''\begin{wrapfigure}{%s}{%s}
%s
\end{wrapfigure}''' % (position_flag, wrapsize, env_content_tex)
    else:
        fig_env_tex = r'''\begin{figure}[%s]
%s
\end{figure}''' % (position_flag, env_content_tex)


    return as_markup_latex(fig_env_tex)


# DO NOT RENAME THIS FUNCTION (required by j2cli)
def j2_environment_params():
    # Jinja2 Environment configuration hook
    # http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment
    return dict()

# DO NOT RENAME THIS FUNCTION (required by j2cli)
def j2_environment(env):
    # Make the function include_file_raw available in the templates
    # as {{ include_file_raw(filename) }}
    env.globals['include_file_raw'] = include_file_raw

    env.globals['ej'] = exercise_marker
    env.globals['proj'] = project_marker
    env.globals['diagram_graphviz'] = diagram_graphviz
    env.globals['figure_fig'] = figure_fig

# DO NOT RENAME THIS FUNCTION (required by j2cli)
def extra_tests():
    """ Declare some custom tests

        Returns: dict(name = function)
    """
    true_kind = ('true', '1', 'y', 'yes')
    false_kind = ('false', '0', 'n', 'no')

    def is_on(n):
        n = str(n).lower()
        if n in true_kind:
            return True
        if n in false_kind:
            return False
        raise Exception("Unknown value '%s'" % n)

    return dict(
        # Example: {% if a is on %}It is on!{% endif %}
        on=lambda n: is_on(n),
        off=lambda n: not is_on(n)
    )
