from django.urls import path
from .views import create_inventory_default

app_name = 'inventory_default'

urlpatterns = [
    path("create/", create_inventory_default, name= "create_inventory_default"),
]