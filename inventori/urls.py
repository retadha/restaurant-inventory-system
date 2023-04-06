from django.urls import path
from .views import create_inventory

app_name = 'inventori'

urlpatterns = [
    path("create_inventory/", create_inventory, name= "create_inventory"),
]