from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from request.models import Request, Inventory_Line
from django.shortcuts import render, redirect
from .models import Riwayat
from django.contrib import messages
@login_required(login_url='/login/')
def pembelian(request):
    pembelian = Request.objects.filter(id_gedung__status__exact="0", status="3")
    context = {
        'requests': pembelian

    }

    return render(request, 'riwayat/pembelian.html', context)

@login_required(login_url='/login/')
def pembelian_lines(request):
    lines = Inventory_Line.objects.filter(id_request__id_gedung__status__exact="0", id_request__status__exact="3")
    context = {
        'lines': lines

    }

    return render(request, 'riwayat/lines.html', context)

# Create your views here.
def home_riwayat(request):
    return render(request, "home_riwayat.html")

def list_riwayat_penjualan(request):
    riwayat_penjualan = Riwayat.objects.all()
    response = {'riwayat_penjualan':riwayat_penjualan}
    return render(request, 'list_riwayat_penjualan.html', response)

