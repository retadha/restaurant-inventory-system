from django.urls import path
from .views import list_inventory, update_stok, update_threshold

app_name = 'inventory'

urlpatterns = [
    path('', list_inventory, name="list_inventory"),
    path('update_stok/<int:id>', update_stok, name='update_stok'),
    path('update_threshold/<int:id>', update_threshold, name='update_threshold'),
]