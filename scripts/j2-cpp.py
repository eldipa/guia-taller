
# See https://github.com/kolypto/j2cli
# pip install j2cli

import jinja2

# DO NOT RENAME THIS FUNCTION (required by j2cli)
def j2_environment_params():
    # Jinja2 Environment configuration hook
    # http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment
    return dict(
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
        )

# DO NOT RENAME THIS FUNCTION (required by j2cli)
def j2_environment(env):
    pass

# DO NOT RENAME THIS FUNCTION (required by j2cli)
def extra_tests():
    return {}
