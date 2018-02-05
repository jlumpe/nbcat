"""Modified version of nbconvert app for converting to terminal only.

Documentation for traitlets packages is pretty lacking, tried to figure this out
as best I could from source of NbConvertApp.
"""

from jupyter_core.application import NoStart
from nbconvert.nbconvertapp import NbConvertApp
from traitlets import Unicode, Bool, DottedObjectName, default
from pygments.styles import get_all_styles

from .terminal_exporter import TerminalExporter


# Override aliases
app_aliases = dict(NbConvertApp.aliases)

# These are fixed
del app_aliases['to']
del app_aliases['nbformat']
del app_aliases['writer']

# New aliases
app_aliases['style'] = 'TerminalExporter.syntax_style'


# Override flags
app_flags = dict(NbConvertApp.flags)
del app_flags['stdout']  # This is now the default
del app_flags['inplace']  # Only relevant when converting to notebook format
del app_flags['generate-config']  # Uses nbconvert's, don't want to overwrite.


# New flags
app_flags.update({
	'256color': (
		{'TerminalExporter': {'use_256_colors': True}},
		'Use ANSI 256 color mode. Enabled by default if your terminal supports'
		' it (TERM environment variable is "xterm-256color").'
	),
	'list-styles': (
		{'NbcatApp': {'list_styles': True}},
		'List available syntax highlighting styles.'
	),
})


class NbcatApp(NbConvertApp):

	# Override CLI argument and stuff
	name = 'nbcat'
	aliases = app_aliases
	flags = app_flags

	# Use nbconvert's config file
	@default('config_file_name')
	def _default_config_file_name(self):
		return 'jupyter_nbconvert_config'

	# Override CLI documentation
	# Indentation gets stripped here
	description = Unicode('''
		View contents of notebook files (*.ipynb) in the terminal.

		Extension to the "jupyter nbconvert" application. New options are
		"--256colors", "--style", and "--list-styles". Other options are
		identical.
	''')

	examples = None

	# Override export format to always use terminal
	export_format = Unicode('terminal')

	# Use stdout by default
	writer_class = DottedObjectName(
		'StdoutWriter',
		help=NbConvertApp.writer_class.help,
	).tag(config=True)

	# Seems to be the list of Configurable classes used the the application
	@property
	def classes(self):
		return super().classes + [NbcatApp, TerminalExporter]

	# Triggers listing of Pygments styles instead of converting
	list_styles = Bool(
		False,
		config=True,
		help='List available syntax highlighting styles.',
	)

	def print_styles_list(self):
		"""Print list of Pygments styles."""
		# print(*sorted(get_all_styles()), sep='\n')

		# Run the corresponding command from pygment's CLI, also prints descriptions
		from pygments.cmdline import main
		main(['pygmentize', '-L', 'styles'])

	def start(self):
		# If list_styles flag set, print styles list and quit
		if self.list_styles:
			self.print_styles_list()
			raise NoStart()

		super().start()


main = NbcatApp.launch_instance
