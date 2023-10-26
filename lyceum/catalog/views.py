__all__ = []
from django.http import HttpResponse
from django.shortcuts import render

from catalog import models
import core.utils


def item_list(request):
    template = 'catalog/item_list.html'
    items = models.Item.objects.all()
    context = {'items': items} | core.utils.get_server_time_context()
    return render(request, template, context)


def item_detail(request, item_index):
    template = 'catalog/item.html'
    try:
        item = models.Item.objects.get(pk=item_index)
    except models.Item.DoesNotExist:
        item = None
    context = {'item': item} | core.utils.get_server_time_context()
    return render(request, template, context)


def item_re(request, num):
    return HttpResponse(f'<body>{num}</body>')
