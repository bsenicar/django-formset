from django.forms import fields, forms, models

from formset.richtext import controls
from formset.richtext.widgets import RichTextarea

from testapp.models import AdvertisementModel


class AdvertisementModelForm(models.ModelForm):
    """
    Edit a "rich text" model field
    ------------------------------

    If plain text is not enough we have to fall back on a rich text editor. For this purpose,
    **django-formset** offers a special model field named ``RichTextField``. It stores the content
    from the rich text editor in JSON rather than HTML. This allows us to store additional metadata
    together with the edited text, but requires to transform that data before rendering to HTML.

    .. code-block:: python

        from django.db.models import Model
        from formset.richtext.fields import RichTextField

        class AdvertisementModel(Model):
            text = RichTextField()

    we now use that model to create a Django ModelForm:

    .. code-block:: python

        from django.forms.models import ModelForm
        from .models import AdvertisementModel

        class AdvertisementModelForm(ModelForm):
            class Meta:
                model = AdvertisementModel
                fields = '__all__'

    which can be used in any ModelView.
    """

    class Meta:
        model = AdvertisementModel
        fields = '__all__'


initial_html = """
<p>This is a boring <em>emphasized paragraph</em>.</p>

<div data-type="draggable-item">
  <p>Followed by a fancy draggable item.</p>
</div>

<div data-type="draggable-item">
  <p>And another draggable item.</p>
  <div data-type="draggable-item">
    <p>And a nested one.</p>
      <div data-type="draggable-item">
        <p>But can we go deeper?</p>
      </div>
  </div>
</div>

<p>Let's finish with a boring <strong>bold paragraph</strong>.</p>
"""


class AdvertisementForm(forms.Form):
    """
    Edit a "rich text" form field
    -----------------------------

    If plain text is not enough, we can fall back on a rich text editor. For this purpose,
    **django-formset** offers a special widget named ``RichTextarea``. It can be added to any
    ``CharField`` in our Django form. By specifying a list of control elements, we can configure
    what kind of HTML markup is allowed inside the editor. Here for instance we allow only certain
    tags.

    .. code-block:: python

        from django.forms import forms
        from formset.richtext.widgets import RichTextarea

        class AdvertisementForm(forms.Form):
            text = fields.CharField(
                widget=RichTextarea(control_elements=[
                    controls.Heading([1,2,3]),
                    controls.Bold(),
                    controls.Italic(),
                    controls.Underline(),
                    controls.Separator(),
                    controls.Redo(),
                    controls.Undo(),
                ]),
                initial="<p>Some HTML<p>",
            )

    Please note: Since here we work with a plain text field, the submitted form data contains HTML
    rather than JSON.
    """
    text = fields.CharField(
        widget=RichTextarea(control_elements=[
            controls.Heading([1,2,3]),
            controls.Bold(),
            controls.Italic(),
            controls.Underline(),
            controls.Link(),
            controls.HorizontalRule(),
            controls.Separator(),
            controls.Redo(),
            controls.Undo(),
        ], attrs={'rows': 15}),
        initial=initial_html,
    )
