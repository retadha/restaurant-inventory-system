from django.urls import path
from .views import create_resep, viewall_resep, delete_resep, view_resep

app_name = 'resep'

urlpatterns = [
    path("create_resep/", create_resep, name= "create_resep"),
    path("viewall/", viewall_resep, name= "viewall_resep"),
    path("view/<id_resep>", view_resep, name= "view_resep"),
    path('edit/<id_resep>', delete_resep, name='edit_resep'),
    path('delete/<id_resep>', delete_resep, name='delete_resep'),


]