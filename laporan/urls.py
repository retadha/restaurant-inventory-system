from django.urls import path
from .views import index, pembelian, penjualan

urlpatterns = [
    path('', index),
    path('pembelian/', pembelian, name='laporan_pembelian'),
    path('penjualan/', penjualan, name='laporan_penjualan'),
]