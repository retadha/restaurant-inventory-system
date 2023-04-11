from django.urls import path
from .views import create_inventory, update_stok, update_threshold

app_name = 'inventori'

urlpatterns = [
    path("create_inventory/", create_inventory, name= "create_inventory"),
    path('update_stok/<int:id>', update_stok, name='update_stok'),
    path('update_threshold/<int:id>', update_threshold, name='update_threshold'),
]