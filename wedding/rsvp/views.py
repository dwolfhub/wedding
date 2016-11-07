from django.shortcuts import render
from django.core.mail import send_mail

import requests

from wedding.settings import MAILGUN_API_KEY, MAILGUN_API_DOMAIN, \
    MAILGUN_API_RECIPIENTS
from .models import Person, Invitation
from .forms import PersonForm, PeopleForm


def __send_email(person, people, total):
    message = person.display_name + " just RSVPed"
    if people:
        message += "\n\nThe following people are coming:\n" \
                  + "\n".join(people)
    else:
        message += "\n\nNo one in the party is coming,"

    message += "\n\nThe current total is %d" % total

    key = MAILGUN_API_KEY
    domain = MAILGUN_API_DOMAIN
    recipients = MAILGUN_API_RECIPIENTS

    request_url = 'https://api.mailgun.net/v2/%s/messages' % domain

    requests.post(request_url, auth=('api', key), data={
        'from': 'no-reply@danandchristin.com',
        'to': recipients,
        'subject': 'Hello',
        'text': message
    })


def rsvp(request):
    complete = None
    error = None
    person = None
    person_form = None
    people = None
    people_form = None

    if request.method == 'POST':
        # person form submitted
        if request.POST['form'] == 'person_form':
            person_form = PersonForm(request.POST)
            if person_form.is_valid():
                form_data = person_form.cleaned_data

                try:
                    person = Person.objects.get(
                        first_name__iexact=form_data['first_name'],
                        last_name__iexact=form_data['last_name'],
                        invitation__zip_code=form_data['zip_code'],
                    )

                    people = person.invitation.person_set.all()

                    coming = []
                    for peep in people:
                        if peep.coming:
                            coming.append(str(peep.id))

                    people_choices = (
                        (person.id, person.first_name + ' ' + person.last_name)
                        for person in people
                    )

                    people_form = PeopleForm(people_choices, {
                        'person': person.id,
                        'invitation': person.invitation_id,
                        'people': coming
                    })

                except Person.DoesNotExist:
                    error = "<strong>Oops!</strong> We didn't recognize your " \
                            "information. Make sure you are using the zip " \
                            "code found on your invitation."

        # people form submitted
        if request.POST['form'] == 'people_form':
            person = Person.objects.get(id=request.POST['person'])

            people = Invitation.objects.get(
                id=request.POST['invitation']).person_set.all()
            people_choices = (
                (person.id, person.first_name + ' ' + person.last_name)
                for person in people)

            people_form = PeopleForm(people_choices, request.POST)
            if people_form.is_valid():
                complete = True

                form_data = people_form.cleaned_data

                for peep in people:
                    if str(peep.id) in form_data['people']:
                        peep.coming = True
                    else:
                        peep.coming = False

                    peep.save()

                total_complete = Person.objects.filter(coming=True).count()

                __send_email(
                    person,
                    [peep.display_name for peep in people if peep.coming],
                    total_complete
                )

    else:
        # neither form submitted
        person_form = PersonForm()

    return render(request, 'rsvp/rsvp.html', {
        'body_class': request.resolver_match.url_name,

        'person': person,
        'person_form': person_form,

        'people': people,
        'people_form': people_form,

        'error': error,
        'complete': complete,
    })
