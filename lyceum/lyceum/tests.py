__all__ = []
from django.test import Client, TestCase
from parameterized import parameterized


class TextReverseMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()

    @parameterized.expand([(True, 9, 1), (False, 10, 0)])
    def test_reverse_russian_words(
        self,
        allow_reverse,
        expected_count,
        expected_reversed_count,
    ):
        with self.settings(ALLOW_REVERSE=allow_reverse):
            responses = []
            for _ in range(10):
                response = self.client.get('/coffee/')
                responses.append(response.content)

            self.assertTrue(
                responses.count('Я чайник'.encode()) == expected_count,
            )
            text_reverse = 'Я кинйач'.encode()
            self.assertTrue(
                responses.count(text_reverse) == expected_reversed_count,
            )
