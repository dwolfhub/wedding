from django.test import TestCase, Client


class TestRoutes(TestCase):
    def test_save_the_date(self):
        response = Client().get('/')
        self.assertEqual(200, response.status_code)

    def test_hotels(self):
        response = Client().get('/hotels')
        self.assertEqual(200, response.status_code)

        response = Client().get('/hotels.html')
        self.assertEqual(301, response.status_code)

    def test_wedding_day_info(self):
        response = Client().get('/wedding-day-info')
        self.assertEqual(200, response.status_code)

        response = Client().get('/wedding-day-info.html')
        self.assertEqual(301, response.status_code)

