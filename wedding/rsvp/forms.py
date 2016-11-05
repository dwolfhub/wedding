from django import forms


class PersonForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=25,
        required=True
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=25,
        required=True
    )
    zip_code = forms.CharField(
        label='Zip Code',
        max_length=6,
        required=True
    )
