"""Setuptools installation script for nbconvert-terminal package."""

import os
from setuptools import setup, find_packages


# Directory of script
root_dir = os.path.dirname(__file__)


# Read readme file for long description
with open(os.path.join(root_dir, 'README.md')) as fobj:
	long_description = fobj.read()


VERSION = '0.0.1'


setup(
	name='nbconvert-terminal',
	version=VERSION,
	description='Jupyter nbconvert extension for viewing notebooks in the terminal.',
	long_description=long_description,
	author='Jared Lumpe',
	url='https://github.com/jlumpe/nbconvert-terminal',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'nbconvert~=5.3',
		'pygments~=2.2',
	],
	entry_points={
		'console_scripts': [
			'jupyter-nbview = nbconvert_terminal.app:main',
		],
		'nbconvert.exporters': [
			'terminal = nbconvert_terminal:TerminalExporter',
		],
	},
	include_package_data=True,
)
