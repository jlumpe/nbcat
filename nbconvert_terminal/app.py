"""Modified version of nbconvert app for converting to terminal only.

Documentation for traitlets packages is pretty lacking, tried to figure this out
as best I could from source of NbConvertApp.
"""

from jupyter_core.application import NoStart
from nbconvert.nbconvertapp import NbConvertApp
from traitlets import Unicode, Bool, DottedObjectName
from pygments.styles import get_all_styles

from .exporter import TerminalExporter


# Override aliases
app_aliases = dict(NbConvertApp.aliases)

# These are fixed
del app_aliases['to']
del app_aliases['nbformat']

# This is overridden, use name of new class
app_aliases['writer'] = 'NbTerminalApp.writer_class'

app_aliases['style'] = 'TerminalExporter.syntax_style'


# Override flags
app_flags = dict(NbConvertApp.flags)
del app_flags['stdout']  # This is now the default
del app_flags['inplace']  # Only relevant when converting to notebook format

# New flags
app_flags.update({
	'256colors': (
		{'TerminalExporter': {'use_256_colors': True}},
		'Use ANSI 256 color mode.',
	),
	'list-styles': (
		{'NbTerminalApp': {'list_styles': True}},
		'List available syntax highlighting styles.'
	),
})


class NbTerminalApp(NbConvertApp):

	# Override CLI argument and stuff
	name = 'jupyter-nbview'
	aliases = app_aliases
	flags = app_flags

	# Override CLI documentation
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
		return super().classes + [NbTerminalApp, TerminalExporter]

	# Triggers listing of Pygments styles instead of converting
	list_styles = Bool(
		False,
		config=True,
		help='List available syntax highlighting styles.',
	)

	def print_styles_list(self):
		"""Print list of Pygments styles."""
		print(*sorted(get_all_styles()), sep='\n')

	def start(self):
		# If list_styles flag set, print styles list and quit
		if self.list_styles:
			self.print_styles_list()
			raise NoStart()

		super().start()
