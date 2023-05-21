from django.urls import path
from riwayat.views import pembelian, pembelian_lines

app_name = 'riwayat'

urlpatterns = [
    path("pembelian", pembelian, name="pembelian"),
    path("pembelian-lines", pembelian_lines, name="pembelian_lines"),


]