"""Define :class:`nbconvert.Exporter` subclass for terminal output."""

import os
import os.path

from traitlets import Bool, Unicode, validate, TraitError
from traitlets.config import Config
from nbconvert.exporters import TemplateExporter
from pygments import highlight
from pygments.formatters import TerminalFormatter, Terminal256Formatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles


# ANSI color reset
ANSI_RESET = '\x1b[0m'

_ansi_color_digits = {
	'black': '0',
	'red': '1',
	'green': '2',
	'yellow': '3',
	'blue': '4',
	'purple': '5',
	'cyan': '6',
	'white': '7',
}

# ANSI control sequences for FG colors
ANSI_COLORS = {}

for name, digit in _ansi_color_digits.items():
	ANSI_COLORS[name] = '\x1b[3' + digit + 'm'
	ANSI_COLORS['b' + name] = '\x1b[9' + digit + 'm'  # Bright


def ansi_color_filter(text, color):
	"""Jinja2 filter which applies ANSI color codes to text."""
	return ANSI_COLORS[color] + str(text) + ANSI_RESET


def make_syntax_highlight_filter(FormatterCls, default_style):
	def syntax_highlight_filter(code, lexername='python3', style=default_style, trim=True):
		lexer = get_lexer_by_name(lexername)

		if trim:
			code = code.strip()

		out = highlight(code, lexer, FormatterCls(style=style))

		if trim:
			out = out.strip()

		return out

	return syntax_highlight_filter


class TerminalExporter(TemplateExporter):
	"""Exporter for viewing notebook in terminal with ANSI colors."""

	output_mimetype = 'text/x-ansi'

	use_256_colors = Bool(
		default_value=False,
		config=True,
		help='Use ANSI 256 color mode',
	)
	syntax_style = Unicode(
		default_value='default',
		config=True,
		help='Pygments style name for coloring output. Only works in 256 color mode',
	)

	@validate('syntax_style')
	def _validate_syntax_style(self, proposal):
		style = proposal['value']
		if style not in get_all_styles():
			raise TraitError('{!r} is not a valid pygments style'.format(style))

		return style

	def _file_extension_default(self):
		return '.txt'

	@property
	def template_path(self):
		templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
		return super().template_path + [templates_dir]

	@property
	def environment(self):
		env = super().environment

		# ANSI escape sequences
		env.globals['RESET'] = ANSI_RESET

		for name, code in ANSI_COLORS.items():
			env.globals[name.upper()] = code

		env.filters['color'] = ansi_color_filter

		# Syntax highlighting filter
		FormatterCls = Terminal256Formatter if self.use_256_colors else TerminalFormatter
		env.filters['syntax'] = make_syntax_highlight_filter(FormatterCls, self.syntax_style)

		return env

	def _template_file_default(self):
		return 'terminal.tpl'

	@property
	def default_config(self):
		c = Config({
			'ExtractOutputPreprocessor': {'enabled': True}
		})
		c.merge(super().default_config)
		return c
