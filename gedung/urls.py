from django.urls import path
from .views import list_gedung, create_gedung, update_gedung, delete_gedung

urlpatterns = [
    path('', list_gedung, name="list_gedung"),
    path('create/', create_gedung, name="create_gedung"),
    path('update/<int:gedung_id>/', update_gedung, name="update_gedung"),
    path('delete/<int:gedung_id>/', delete_gedung, name="delete_gedung"),
]
