from django.urls import path
from .views import create_inventory_default, delete

app_name = 'inventory_default'

urlpatterns = [
    path("create/", create_inventory_default, name= "create_inventory_default"),
    path('delete/<id_inventory_default>', delete, name='delete'),
]