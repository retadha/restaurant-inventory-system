from django.urls import path
from .views import pembelian

urlpatterns = [
    # path('', views.index),
    path('pembelian/', pembelian, name='pembelian'),
]