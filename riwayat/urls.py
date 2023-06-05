from django.urls import path
from riwayat.views import pembelian, pembelian_lines
from .views import list_riwayat_penjualan, home_riwayat
app_name = 'riwayat'

urlpatterns = [
    path("pembelian", pembelian, name="pembelian"),
    path("pembelian-lines", pembelian_lines, name="pembelian_lines"),
    path('', home_riwayat, name='home_riwayat'),
    path('penjualan/', list_riwayat_penjualan, name='penjualan')
]