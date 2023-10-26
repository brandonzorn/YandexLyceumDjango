__all__ = []
from http import HTTPStatus


from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get('/about/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ReverseURLTests(TestCase):
    def test_item_detail_reverse_url(self):
        url = reverse('about:description')
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
