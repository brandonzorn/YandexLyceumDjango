__all__ = []
from django.http import HttpResponse
from django.shortcuts import render

from catalog import models


def item_list(request):
    template = 'catalog/item_list.html'
    items = models.Item.objects.all()
    context = {'items': items}
    return render(request, template, context)


def item_detail(request, item_index):
    template = 'catalog/item.html'
    try:
        item = models.Item.objects.get(pk=item_index)
    except models.Item.DoesNotExist:
        item = None
    context = {'item': item}
    return render(request, template, context)


def item_re(request, num):
    return HttpResponse(f'<body>{num}</body>')
