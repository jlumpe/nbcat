"""Setuptools installation script for nbcat package."""

import os
from setuptools import setup, find_packages


# Directory of script
root_dir = os.path.dirname(__file__)


# Read readme file for long description
with open(os.path.join(root_dir, 'README.md')) as fobj:
	long_description = fobj.read()


VERSION = '0.0.1'


setup(
	name='nbcat',
	version=VERSION,
	description='Print formatted contents of Jupyter notebooks to the terminal.',
	long_description=long_description,
	author='Jared Lumpe',
	url='https://github.com/jlumpe/nbcat',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'nbconvert~=5.3',
		'pygments~=2.2',
	],
	entry_points={
		'console_scripts': [
			'nbcat = nbcat.app:main',
		],
		'nbconvert.exporters': [
			'terminal = nbcat:TerminalExporter',
		],
	},
	include_package_data=True,
)
