from django.urls import path
from .views import create_resep

urlpatterns = [
    path("create_resep/", create_resep, name= "create_resep")
]