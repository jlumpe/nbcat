{% extends 'null.tpl' %}


{# Macro for section headers #}
{% macro section(text, col='bblack') -%}
{{ ('---- [' + text + '] ----') | color(col) }}
{%- endmacro %}

{% macro end_section(col='bblack') -%}
{{ ('---- / ----') | color(col) }}
{%- endmacro %}


{# Macro for In[] and Out[] prompts #}
{% macro prompt(cell, text, color1, color2) -%}
{{- (text + '[') | color(color1) -}}
{{- cell.execution_count | replace(None, ' ') | color(color2) -}}
{{- ']:' | color(color1) -}}
{%- endmacro %}


{# Blank lines between cells #}
{% block any_cell -%}
{{ super() }}


{% endblock any_cell %}


{# Customize prompts to match IPython terminal #}
{% block in_prompt -%}
{{ prompt(cell, 'In', 'green', 'bgreen') }}
{%- if nb.metadata.language_info -%}
{{ (' (' + nb.metadata.language_info.name + ')') | color('bblack') }}
{%- endif %}
{%- endblock in_prompt %}


{% block output_prompt -%}
{{ prompt(cell, 'Out', 'red', 'bred') }}
{%- endblock output_prompt %}


{# Input with syntax highlighting #}
{% block input %}
{{ cell.source | syntax | indent }}
{% endblock input %}


{% block outputs %}
{{- super() | indent -}}
{% endblock outputs %}


{# Execution result #}
{% block execute_result scoped %}
{{ section('>>>') }}
{{ output.data['text/plain'] }}
{%- endblock execute_result %}


{# Stream output #}
{% block stream_stdout %}
{{ section('stdout') }}
{{ output.text | trim }}
{%- endblock stream_stdout %}


{% block stream_stderr %}
{{ section('stderr') }}
{{ output.text | trim | color('bred') }}
{%- endblock stream_stderr %}


{# Markdown cells with syntax highlighting #}
{% block markdowncell scoped -%}
{{ section('md', 'bblue') }}
{{ cell.source | syntax('md') | indent }}
{{ end_section('bblue') }}
{%- endblock markdowncell %}


{# Don't strip ANSI codes from traceback lines #}
{% block traceback_line %}
{{ line }}
{% endblock traceback_line %}
