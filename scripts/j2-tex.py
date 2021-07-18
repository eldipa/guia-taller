
# See https://github.com/kolypto/j2cli
# pip install j2cli

import jinja2

@jinja2.contextfunction
def include_file_raw(ctx, name):
    ''' Function to open and read the given file (<name>) and
        return its content as-is (raw). Jinja will not try to
        parse it in any way.

        This contrast with Jinja's include tag ({% include fname %})
        which process the file as a Jinja template before returning
        it.
    '''
    env = ctx.environment
    return jinja2.Markup(env.loader.get_source(env, name)[0])

# DO NOT RENAME THIS FUNCTION (required by j2cli)
def j2_environment_params():
    # Jinja2 Environment configuration hook
    # http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment
    return dict(
        # Change the blocks' start/end markers
        # from  {% xxx %}  to  ~% xxx %~
        # (required to not enter in conflict with Tex syntax)
        block_start_string='~%',
        block_end_string='%~',

        # Change the variables' start/end markers
        # from  {{ xxx }}  to  ~{ xxx }~
        # (required to not enter in conflict with Tex syntax)
        variable_start_string='~{',
        variable_end_string='}~',

	# Change the comments' start/end/markers
        # from  {# xxx #}  to  ~# xxx #~
        # (required to not enter in conflict with Tex syntax)
	comment_start_string='~#',
	comment_end_string='#~'
    )

# DO NOT RENAME THIS FUNCTION (required by j2cli)
def j2_environment(env):
    # Make the function include_file_raw available in the templates
    # as {{ include_file_raw(filename) }}
    # (or ~{ include_file_raw(filename) }~ to be more precise)
    env.globals['include_file_raw'] = include_file_raw

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
