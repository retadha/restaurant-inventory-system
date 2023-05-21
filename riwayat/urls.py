from django.urls import path
from .views import list_riwayat_penjualan, home_riwayat

urlpatterns=[
    path('', home_riwayat, name='home_riwayat'),
    path('list_riwayat_penjualan/', list_riwayat_penjualan, name='list_riwayat_penjualan')
]