from django.urls import path
from .views import create_supplier

urlpatterns=[
    path('create_supplier/', create_supplier, name='create_supplier')
]