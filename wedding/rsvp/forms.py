from django import forms


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
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    message = forms.CharField(
        widget=forms.Textarea,
        label="Leave a message for the Bride and Groom",
        required=False
    )

    def __init__(self, people, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        self.fields['people'].choices = people