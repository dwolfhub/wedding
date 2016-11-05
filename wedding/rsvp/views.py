from django.shortcuts import render

from .models import Person
from .forms import PersonForm


def rsvp(request):
    form_data = {}

    if request.method == 'POST':
        person_form = PersonForm(request.POST)
        if person_form.is_valid():
            form_data = person_form.cleaned_data

            try:
                people = Person.objects.get(
                    first_name__iexact=form_data['first_name'],
                    last_name__iexact=form_data['last_name'],
                    invitation__zip_code=form_data['zip_code'],
                ).invitation.person_set.all()

            except Person.DoesNotExist:
                print('ok')



    else:
        person_form = PersonForm()

    return render(request, 'rsvp/rsvp.html', {
        'body_class': request.resolver_match.url_name,
        'form_data': form_data,
        'person_form': person_form,
    })
