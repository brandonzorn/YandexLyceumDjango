__all__ = []
from django.shortcuts import render

import core.utils


def description(request):
    template = 'about/about.html'
    context = core.utils.get_server_time_context()
    return render(request, template, context)
