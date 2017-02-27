from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class DropdownChoiceInput(forms.widgets.ChoiceInput):
    input_type = 'dropdown'

    def __init__(self, *args, **kwargs):
        super(DropdownChoiceInput, self).__init__(*args, **kwargs)
        self.value = set(force_text(v) for v in self.value)

    def is_checked(self):
        return self.choice_value in self.value

    def render(self, name=None, value=None, attrs=None):
        coming, not_coming = '', ''
        if self.is_checked():
            coming = 'selected="selected"'
        else:
            not_coming = 'selected="selected"'

        return format_html(
            '<label>{}</label>'
            '<div class="select-wrapper">'
            '<select name="people-{}">'
            '<option value="" {}>cannot attend</option>'
            '<option value="{}" {}>will be attending</option>'
            '</select>'
            '</div><div class="clearfix"></div>'.format(self.choice_label,
                                                        self.index, not_coming,
                                                        self.choice_value,
                                                        coming)
        )


class DropdownFieldRenderer(forms.widgets.ChoiceFieldRenderer):
    choice_input_class = DropdownChoiceInput

    outer_html = '<div{id_attr} class="form-width-wrapper">{content}</div>'
    inner_html = '{choice_value}{sub_widgets}'


class DropdownSelectMultiple(forms.widgets.RendererMixin, forms.SelectMultiple):
    renderer = DropdownFieldRenderer

    def value_from_datadict(self, data, files, name):
        if isinstance(data, forms.widgets.MultiValueDict):
            people = []
            for key, val in data.items():
                if 'people-' in key and val:
                    people.append(val)
            return people
        else:
            return data.get(name)


class Dropdown(forms.Select):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<div class="select-wrapper"><select{}>',
                              flatatt(final_attrs))]
        options = self.render_options([value])
        if options:
            output.append(options)
        output.append('</select></div>')
        return mark_safe('\n'.join(output))


class PersonForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=25,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=25,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    zip_code = forms.CharField(
        label='Zip Code',
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )


class PeopleForm(forms.Form):
    invitation = forms.CharField(
        widget=forms.HiddenInput,
    )
    person = forms.CharField(
        widget=forms.HiddenInput,
    )
    people = forms.MultipleChoiceField(
        widget=DropdownSelectMultiple(),
        required=False
    )
    shuttle = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')),
                                label='Will you be taking the shuttle to and '
                                      'from The Abbey Resort to the venue?',
                                initial='',
                                widget=Dropdown(), required=True)
    message = forms.CharField(
        widget=forms.Textarea,
        label="Leave a message for the Bride and Groom",
        required=False
    )

    def __init__(self, people, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        self.fields['people'].choices = people
