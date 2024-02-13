from django.utils.html import format_html

# from formset.renderers import ButtonVariant, ClassList
from formset.renderers.default import FormRenderer as DefaultFormRenderer

class FormRenderer(DefaultFormRenderer):
    max_options_per_line = 4
    framework = 'materialize'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    _template_mapping = dict(DefaultFormRenderer._template_mapping, **{
        'django/forms/div.html': 'formset/materialize/form.html',
        'django/forms/default.html': 'formset/materialize/form.html',
    })
