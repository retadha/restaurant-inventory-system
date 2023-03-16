from django.urls import path
from .views import create_supplier, list_supplier

urlpatterns=[
    path('create_supplier', create_supplier, name='create_supplier'),
    path('list_supplier', list_supplier, name='list_supplier')
]