{% extends 'null.tpl' %}


{# Macro for section headers #}
{% macro section_head(text, col='bblack') -%}
{{ ('---- [' + text + '] ----') | color(col) }}
{%- endmacro %}

{% macro section_tail(text, col='bblack') -%}
{{ ('---- /' + text + '  ----') | color(col) }}
{%- endmacro %}

{% macro section(text, col='bblack') -%}
{{ section_head(text, col) }}
{{ caller() }}
{{ section_tail(text, col) }}
{%- endmacro %}


{# Macro for In[] and Out[] prompts #}
{% macro prompt(cell, text, color1, color2) -%}
{{- (text + '[') | color(color1) -}}
{{- cell.execution_count | replace(None, ' ') | color(color2) -}}
{{- ']:' | color(color1) -}}
{%- endmacro %}


{# Two blank lines between cells #}
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
{{ cell.source | syntax | trim | indent }}

{% endblock input %}


{# Execution result #}
{% block execute_result scoped %}
{%- if cell.outputs | length > 1 %}
{{ '>>>' | color('bblack') }}
{%- endif %}
{{ output.data['text/plain'] | indent }}
{%- endblock execute_result %}


{# Stream output #}
{% block stream_stdout %}
{{ '[stdout]' | color('bblack') }}
{{ output.text | trim | indent }}
{%- endblock stream_stdout %}


{% block stream_stderr %}
{{ '[stderr]' | color('bblack')  }}
{{ output.text | trim | color('bred') | indent }}
{%- endblock stream_stderr %}


{# Markdown cells with syntax highlighting #}
{% block markdowncell scoped -%}
{% call section('md', 'bblue') -%}
{{ cell.source | syntax('md') | indent }}
{%- endcall  %}
{%- endblock markdowncell %}

{% block rawcell scoped -%}
{% call section('raw', 'cyan') -%}
{{ cell.source | indent }}
{%- endcall %}
{%- endblock rawcell %}


{# Don't strip ANSI codes from traceback lines #}
{% block traceback_line %}
{{ line }}
{% endblock traceback_line %}
