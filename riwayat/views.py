from django.shortcuts import render, redirect
from .models import Riwayat
from django.contrib import messages

# Create your views here.
def home_riwayat(request):
    return render(request, "home_riwayat.html")

def list_riwayat_penjualan(request):
    riwayat_penjualan = Riwayat.objects.all()
    response = {'riwayat_penjualan':riwayat_penjualan}
    return render(request, 'list_riwayat_penjualan.html', response)