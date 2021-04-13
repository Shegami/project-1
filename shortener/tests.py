from django.test import TestCase
from shortener.models import Shortener
from datetime import date
from shortener.views import click_counter, \
    is_user_url, is_available, generate_url
from unittest import mock


class HomeTest(TestCase):
    def test_home(self):
        result = self.client.get('/')
        TestCase.assertEqual(self, result.status_code, 200)


class CreateModelTest(TestCase):
    def setUp(self):
        Shortener.objects.create(
            full_url='https://www.onliner.by/',
            short_url='http://127.0.0.1:8000/TEST'
        )

    def test_create_model(self):
        model = Shortener.objects.get(short_url='http://127.0.0.1:8000/TEST')
        create_date = model.create_date
        clicks = model.clicks
        self.assertEqual(create_date, date.today())
        self.assertEqual(clicks, 0)


class ClicksTest(TestCase):
    def setUp(self):
        Shortener.objects.create(
            full_url='https://www.onliner.by/',
            short_url='http://127.0.0.1:8000/TEST'
        )

    def test_click_counter(self):
        model = Shortener.objects.get(id=1)
        self.assertEqual(model.clicks, 0)
        click_counter(request=None,
                      link_id=model.id)
        model = Shortener.objects.get(id=1)
        self.assertEqual(model.clicks, 1)


class NoUserUrlTest(TestCase):
    @mock.patch('shortener.views.generate_url', return_value='TEST')
    def test_is_user_url(self, user_url=''):
        result = is_user_url(user_url)
        self.assertEqual(result, 'TEST')


class UserUrlTest(TestCase):
    def test_is_user_url(self, user_url='ALPHABET'):
        result = is_user_url(user_url)
        self.assertEqual(
            result,
            'http://127.0.0.1:8000/ALPHABET'
        )


class IsAvailableTest(TestCase):
    def setUp(self):
        Shortener.objects.create(
            full_url='https://www.onliner.by/',
            short_url='http://127.0.0.1:8000/TEST'
        )

    def test_is_available(self):
        result = is_available(short_url='http://127.0.0.1:8000/TEST')
        self.assertEqual(result, False)
        result = is_available(short_url='http://127.0.0.1:8000/TEST01')
        self.assertEqual(result, 'http://127.0.0.1:8000/TEST01')


class GenerateUrlTest(TestCase):
    @mock.patch('shortener.views.choices', return_value=['T', 'e', 'S', 't', '0', '1'])
    def test_generate_no_url(self, choices_patch):
        result = generate_url()
        self.assertEqual(result, 'http://127.0.0.1:8000/TeSt01')

    def test_generate_url(self):
        result = generate_url(user_url='ALPHABET')
        self.assertEqual(result, 'http://127.0.0.1:8000/ALPHABET')


class FullLink(TestCase):
    def setUp(self):
        Shortener.objects.create(
            full_url='https://www.onliner.by/',
            short_url='http://127.0.0.1:8000/TEST'
        )

    def test_full(self):
        model = Shortener.objects.get(id=1)
        result = self.client.get(model.full_url)
        TestCase.assertEqual(self, result.status_code, 200)
