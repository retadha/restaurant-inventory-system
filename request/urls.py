from django.urls import path
from .views import list

app_name = 'request'

urlpatterns = [
    path("", list, name="list"),

]