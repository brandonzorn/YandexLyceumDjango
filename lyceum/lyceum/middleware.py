__all__ = []
import re

from django.conf import settings
from django.core.cache import cache


class ReverseRussianWordsMiddleware:
    _counter = cache.get('reverse_middleware_counter') or 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._counter += 1
        response = self.get_response(request)
        if settings.ALLOW_REVERSE and self._counter % 10 == 0:
            response.content = self.reverse_words(response.content)
            self._counter = 0
        cache.set('reverse_middleware_counter', self._counter)
        return response

    def reverse_words(self, content):
        content = content.decode('utf-8')
        pattern = r'[а-яА-ЯёЁ]+'
        reversed_words = re.sub(pattern, lambda x: x.group(0)[::-1], content)
        return reversed_words
