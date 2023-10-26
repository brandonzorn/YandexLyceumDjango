from django.urls import path, re_path, register_converter

from catalog import converters, views


app_name = 'catalog'

register_converter(converters.PositiveNumber, 'pint')

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:item_index>/', views.item_detail, name='item_detail'),
    re_path(r'^re/(?P<num>[1-9]\d*)/$', views.item_re, name='item_re'),
    path('converter/<pint:num>/', views.item_re),
]
