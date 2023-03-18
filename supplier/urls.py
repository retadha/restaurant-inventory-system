from django.urls import path
from .views import create_supplier, list_supplier, update_supplier, get_supplier, delete_supplier

urlpatterns=[
    path('create_supplier', create_supplier, name='create_supplier'),
    path('list_supplier', list_supplier, name='list_supplier'),
    path('update_supplier', update_supplier, name='update_supplier'),
    path('get_supplier', get_supplier, name='get_supplier'),
    path('delete_supplier', delete_supplier, name='delete_supplier')
]