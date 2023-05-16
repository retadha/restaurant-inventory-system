from django.urls import path
from .views import create, list, delete, view, update

app_name = 'resep'

urlpatterns = [
    path("create", create, name="create"),
    path("", list, name="list"),
    path("<id_resep>", view, name="view"),
    path('update/<id_resep>', update, name='update'),
    path('delete/<id_resep>', delete, name='delete'),


]