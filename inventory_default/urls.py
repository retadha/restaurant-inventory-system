from django.urls import path
from .views import list_inventory_default, create_inventory_default, update, delete

app_name = 'inventory_default'

urlpatterns = [
    path('', list_inventory_default, name="list_inventory_default"),
    path("create/", create_inventory_default, name="create_inventory_default"),
    path('update/<int:id_inventory_default>/', update, name="update_inventory_default"),
    path('delete/<int:id_inventory_default>', delete, name='delete_inventory_default'),
]