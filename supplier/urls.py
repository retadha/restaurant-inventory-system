from django.urls import path
from .views import create_supplier, list_supplier, update_supplier, get_supplier, delete_supplier

urlpatterns=[
    path('', list_supplier, name='list_supplier'),
    path('create_supplier/', create_supplier, name='create_supplier'),
    path('update_supplier/<int:id>', update_supplier, name='update_supplier'),
    path('get_supplier/<int:id>', get_supplier, name='get_supplier'),
    path('delete_supplier/<int:id>', delete_supplier, name='delete_supplier')
]