from django.test import TestCase, Client
from .models import Invitation, Person


class TestPersonForm(TestCase):
    def setUpTestData():
        invite = Invitation(title='John and Jane Doe', zip_code=88888)
        invite.save()

        person = Person(first_name='John', last_name='Doe',
                        display_name='Uncle John', invitation_id=invite.token,
                        coming=False)
        person.save()

        person_2 = Person(first_name='Jane', last_name='Doe',
                          display_name='Aunt Jane', invitation_id=invite.token,
                          coming=False)
        person_2.save()

    def test_page_loads_shows_form(self):
        response = Client().get('/rsvp')
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(
            -1,
            str(response.content).find('person-lookup-form')
        )

    def test_invalid_form_fields(self):
        response = Client().post('/rsvp', {
            'some': 'bad',
            'data': 'here',
        })
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(
            -1,
            str(response.content).find('person-lookup-form')
        )

    def test_invalid_person_details(self):
        response = Client().post('/rsvp', {
            'first_name': 'jerry',
            'last_name': 'smith',
            'zip_code': '78987',
            'form': 'person_form',
        })

        self.assertEqual(200, response.status_code)
        response = str(response.content)
        self.assertNotEqual(
            -1,
            response.find('>Not Found<')
        )
        self.assertNotEqual(
            -1,
            response.find('person-lookup-form')
        )

    def test_valid_person_details(self):
        response = Client().post('/rsvp', {
            'first_name': 'john',
            'last_name': 'doe',
            'zip_code': '88888',
            'form': 'person_form',
        })

        self.assertEqual(200, response.status_code)

        response = str(response.content)
        self.assertNotEqual(
            -1,
            response.find('Hi, Uncle John!')
        )
        self.assertNotEqual(
            -1,
            response.find('people-coming-form')
        )
        self.assertNotEqual(
            -1,
            response.find('id="id_people"')
        )

    def test_invalid_people_data(self):
        c = Client()
        response = c.post('/rsvp', {
            'form': 'people_form'
        })

        self.assertEqual(200, response.status_code)

        response = str(response.content)
        self.assertNotEqual(
            -1,
            response.find('person-lookup-form')
        )

        response = c.post('/rsvp', {
            'form': 'people_form',
            'invitation': '9999999',
            'person': '1',
        })

        response = str(response.content)
        self.assertNotEqual(
            -1,
            response.find('Hi, Uncle John!')
        )

    def test_valid_people_data(self):
        c = Client()
        response = c.post('/rsvp', {
            'form': 'people_form',
            'invitation': '1',
            'person': '1',
            'people': [
                '1', '2'
            ]
        })

        response = str(response.content)
        self.assertNotEqual(
            -1,
            response.find('Thanks for letting us know!')
        )
        self.assertEqual(
            2,
            Person.objects.filter(coming=True).count()
        )

        response = c.post('/rsvp', {
            'form': 'people_form',
            'invitation': '1',
            'person': '1',
            'people': [
                '1'
            ]
        })

        response = str(response.content)
        self.assertNotEqual(
            -1,
            response.find('Thanks for letting us know!')
        )
        self.assertEqual(
            1,
            Person.objects.filter(coming=True).count()
        )

        response = c.post('/rsvp', {
            'form': 'people_form',
            'invitation': '1',
            'person': '1',
            'people': []
        })

        response = str(response.content)
        self.assertNotEqual(
            -1,
            response.find('Thanks for letting us know!')
        )
        self.assertEqual(
            0,
            Person.objects.filter(coming=True).count()
        )

        response = c.post('/rsvp', {
            'form': 'people_form',
            'invitation': '1',
            'person': '1',
        })

        response = str(response.content)
        self.assertNotEqual(
            -1,
            response.find('Thanks for letting us know!')
        )
        self.assertEqual(
            0,
            Person.objects.filter(coming=True).count()
        )


