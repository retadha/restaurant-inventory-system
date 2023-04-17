from django.urls import path
from .views import list, confirm, receive, delete, accept

app_name = 'request'

urlpatterns = [
    path("", list, name="list"),
    path("accept", accept, name='accept'),
    path("confirm/<id_request>", confirm, name='confirm'),
    path("receive/<id_request>", receive, name='receive'),
    path("delete/<id_request>", delete, name='delete'),

]