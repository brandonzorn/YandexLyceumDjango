__all__ = []
from django.http import HttpResponse
from django.shortcuts import render

import core.utils


def home(request):
    template = 'homepage/homepage.html'
    context = core.utils.get_server_time_context()
    return render(request, template, context)


def coffee(request):
    return HttpResponse('Я чайник', status=418)
