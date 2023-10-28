__all__ = []
from django.http import HttpResponse, Http404
from django.shortcuts import render

from catalog import models


def item_list(request):
    template = 'catalog/item_list.html'
    items = models.Item.objects.filter(is_published=True)
    context = {'items': items}
    return render(request, template, context)


def item_detail(request, item_index):
    template = 'catalog/item.html'
    item = models.Item.objects.filter(pk=item_index, is_published=True).first()
    if not item:
        raise Http404
    context = {'item': item}
    return render(request, template, context)


def item_re(request, num):
    return HttpResponse(f'<body>{num}</body>')
