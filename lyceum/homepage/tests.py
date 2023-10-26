__all__ = []
from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_endpoint(self):
        response = Client().get('/coffee/')
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_endpoint_text(self):
        response = Client().get('/coffee/')
        self.assertIn('Я чайник'.encode(), response.content)


class ReverseURLTests(TestCase):
    def test_item_detail_reverse_url(self):
        url = reverse('homepage:home')
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
