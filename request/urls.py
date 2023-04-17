from django.urls import path
from .views import list, confirm, receive

app_name = 'request'

urlpatterns = [
    path("", list, name="list"),
    path("confirm/<id_request>", confirm, name='confirm'),
    path("receive/<id_request>", receive, name='receive')

]