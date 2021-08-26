
# See https://github.com/kolypto/j2cli
# pip install j2cli

import jinja2, re, os

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


def as_markup_latex(tex, block=True):
    if block:
        return jinja2.Markup('```{=latex}\n%s\n```' % tex)
    else:
        # the extra {} makes Tex to separate the tex code from the text
        # that follows to the right
        return jinja2.Markup('%s{}' % tex)

exercise_or_project_marker = r'''\stepcounter{%(countername)s} \subsubsection{%(prefix)s \arabic{chapter}.\arabic{%(countername)s}: %(title)s}'''

@jinja2.contextfunction
def exercise_marker(ctx, hazard=False, tricky=False):
    tag = ''
    if tricky:
        tag += '↯'
    if hazard:
        tag += '☣'

    prefix = 'Ej'
    if tag:
        prefix = tag + ' ' + prefix

    content = exercise_or_project_marker % dict(prefix=prefix, countername='exercisecounter', title='')
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
def _diagrams__graphviz(ctx, src, **kargs):
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
def _figures__fig(ctx, path, position='here', caption='', captionpos='bottom',
        figparams={}, wrapsize=r'0.25\textwidth'):
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

@jinja2.contextfunction
def _boxes__extra_footage_begin(ctx):
    # Options:
    #   enhanced jigsaw: needed to not draw a closed box on each page
    #   when the extra_footage spans multiple pages. Instead draw each
    #   to make the illusion that the box continues in the next page.
    #
    #   breakable: needed otherwise extra_footage larger than a page
    #   will not span multiple pages
    #
    #   before upper: [weird] don't collapse the paragraphs in
    #   the extra_footage.
    flags = 'title={Extra footage},enhanced jigsaw,breakable,before upper=\setlength{\parskip}{1em}'
    return as_markup_latex(r'''\begin{tcolorbox}[%s]''' % flags)

@jinja2.contextfunction
def _boxes__extra_footage_end(ctx):
    return as_markup_latex(r'''\end{tcolorbox}''')


@jinja2.contextfunction
def include_block(ctx, name, block, strip=True, indent=0, compact=True, ctx_env={}):
    ''' Function to open and read the given file (<name>), see it
        as a Jinja template, get the named block (<block>) and
        evaluate it with the given context <ctx_env>.

        Then return it as is.

        If <block> is None, grab the whole file.

        If <strip> is given, the left indentation is removed from the
        lines but preserving the overall indentation.

        If <indent> is given, that amount of space is added on the left.

        If <compact> is given, all the first and last lines that are
        empty are removed.

        Example:

            {{ include_block(src_dir + "/" + fname, "header") }}
    '''
    # This special environment is for processing C/C++ files
    # because we cannot use the Environment for Mardown files
    env = jinja2.Environment(
        # Change the blocks' start/end markers
        # from  {% xxx %}  to  /*% xxx %*/
        # In this way, they look like C/C++ comments
        block_start_string='/*%',
        block_end_string='%*/',

        # Change the variables' start/end markers
        # from  {{ xxx }}  to  /*{ xxx }*/
        variable_start_string='/*{',
        variable_end_string='}/*',

	# Change the comments' start/end/markers
        # from  {# xxx #}  to  /*# xxx #*/
	comment_start_string='/*#',
	comment_end_string='#*/',

        loader=ctx.environment.loader
    )

    # Get the template
    template = env.get_template(name)

    if block == None:
        content = template.render(ctx)
    else:
        # Get the named block from the template
        block = template.blocks[block]

        content = jinja2.utils.concat(block(ctx))

    if strip or indent or compact:
        lines = content.split('\n')

        if compact:
            # drop the first lines if they are empty
            while lines and not lines[0].strip():
                lines.pop(0)

            # drop the last lines if they are empty
            while lines and not lines[-1].strip():
                lines.pop()

        if strip:
            # Find the minimum of indentation to strip
            MAX = 9999999
            min_indent = MAX
            for l in lines:
                space = re.match(r'^(\s*)\S', l)
                if space:
                    space = space.group(1)
                    min_indent = min(min_indent, len(space))

            if min_indent < MAX:
                lines = (l[min_indent:] for l in lines)

        if indent:
            indent = ' ' * indent
            lines = (indent + l for l in lines)

        content = '\n'.join(lines)

    return jinja2.Markup(content)

@jinja2.contextfunction
def emoji(ctx, name, path='z/img/emoji'):
    ''' Include inline a small image, typically an emoji.

        The name of the emoji must correspond to the name of the file
        that it is in the given path but it is not necessary to include
        the extension: emoji() will add it by default.

            {{ emoji('rocket') }}

        If the resulting image file does not exist or if there are
        multiple files that correspond to the same name (but different
        extensions), an error is raised.

        In the latter case the ambiguous case can be removed adding the
        extension to the name.

            {{ emoji('rocket.png') }}

        emoji() can be used to include other images that are small
        enough as well. You probably will want to change the default
        path however:

            {{ emoji('rocket.png', 'z/img/icons/') }}
    '''
    path = os.path.join(path, name)
    _, ext = os.path.splitext(path)
    if not ext:
        base = path
        path = None
        for ext in ('.pdf', '.png', '.jpeg', ''):
            if os.path.exists(base + ext):
                if path is not None:
                    raise Exception(f"Emoji path is ambiguous. Is '{base + ext}' or '{path}'?")
                path = base + ext
    if not os.path.exists(path):
        raise Exception(f"Emoji path does not exist: '{path}'")

    tex = r'\text{\raisebox{-0.2em}{\includegraphics[height=1em]{%s}}}' % path
    return as_markup_latex(tex, block=False)


# DO NOT RENAME THIS FUNCTION (required by j2cli)
def j2_environment_params():
    # Jinja2 Environment configuration hook
    # http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment
    return dict()

# DO NOT RENAME THIS FUNCTION (required by j2cli)
def j2_environment(env):
    # Public functions
    env.globals['include_file_raw'] = include_file_raw
    env.globals['ej'] = exercise_marker
    env.globals['proj'] = project_marker
    env.globals['include_block'] = include_block
    env.globals['emoji'] = emoji

    # Private functions
    env.globals['_diagrams__graphviz'] = _diagrams__graphviz
    env.globals['_figures__fig'] = _figures__fig
    env.globals['_boxes__extra_footage_begin'] = _boxes__extra_footage_begin
    env.globals['_boxes__extra_footage_end'] = _boxes__extra_footage_end

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
