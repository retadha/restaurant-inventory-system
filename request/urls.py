from django.urls import path
from .views import list, confirm, receive, delete, to_process, process, supplier_process, create, update

app_name = 'request'

urlpatterns = [
    path("", list, name="list"),
    path("to_process", to_process, name='to_process'),
    path("process/<id_request>", process, name="process"),
    path("supplier_process/<id_request>", supplier_process, name="supplier_process"),
    path("confirm/<id_request>", confirm, name='confirm'),
    path("receive/<id_request>", receive, name='receive'),
    path("delete/<id_request>", delete, name='delete'),
    path("create", create, name='create'),
    path("update/<id_request>", update, name='update'),
]