__all__ = []
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    template = 'homepage/homepage.html'
    context = {}
    return render(request, template, context)


def coffee(request):
    return HttpResponse('Я чайник', status=418)
