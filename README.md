# nbcat

Extends `jupyter nbconvert` to enable printing the contents of `.ipynb` files to the terminal. You can
use it to easily inspect the contents of notebook files without having to start the notebook server.

## Command line usage

The general form is

    nbcat [--style <style>] notebook.ipynb

where the `--style` option sets the syntax highlighting style to use with [pygments](http://pygments.org/). Use

    nbcat --list-styles

to list all available styles. See the [example](#example) below.


## Installation

Just run `python setup.py install`.


## Configuration

This package uses Jupyter's `nbconvert` system internally and shares the same configuration file.
This is usually in `~/.jupyter/jupyter_nbconvert_config.py`. If it doesn't exist, you can create
it with `nbconvert --generate-config`. Probably the only one worth using is the `syntax_style` trait:

    c.TerminalExporter.syntax_style = 'monokai'


## Details

Note: styles are only enabled in 256 color mode, which is enabled by default if your terminal
emulator supports it. You can also force this using the `--256color` flag.

If you want to page through the output by piping it through `less`, use the `-r` argument:

    nbcat [--style <style>] notebook.ipynb | less -r

The terminal exporter is also registered with the `nbconvert` API, so you can use that command as well:

    jupyter nbconvert -to terminal notebook.ipynb


## Example

Example output for viewing this [example notebook](example/example.ipynb):

    nbcat --style=monokai example/example/ipynb

<img src="example/example.png" width="600px"></img>
