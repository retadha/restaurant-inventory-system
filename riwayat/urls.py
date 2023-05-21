from django.urls import path
from riwayat.views import pembelian

app_name = 'riwayat'

urlpatterns = [
    path("pembelian", pembelian, name="pembelian"),


]