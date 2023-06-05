from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from employee.models import Employee
from propensi.utils import is_manager, is_gudang_pusat
from request.models import Request, Inventory_Line
from django.shortcuts import render, redirect
from django.contrib import messages

class POS_Penjualan:
    def __init__(self, product, total, price, date):
        self.product = product
        self.total = total
        self.price = price
        self.date = date

@login_required(login_url='/login/')
def pembelian(request):
    if not (is_manager(request) and is_gudang_pusat(request)):
        return render(request, 'error/403.html')

    pembelian = Request.objects.filter(id_gedung__status__exact="0", status="3")
    context = {
        'requests': pembelian

    }

    return render(request, 'riwayat/pembelian.html', context)

@login_required(login_url='/login/')
def pembelian_lines(request):
    if not (is_manager(request) and is_gudang_pusat(request)):
        return render(request, 'error/403.html')

    lines = Inventory_Line.objects.filter(id_request__id_gedung__status__exact="0", id_request__status__exact="3")
    context = {
        'lines': lines

    }

    return render(request, 'riwayat/lines.html', context)

@login_required(login_url='/login/')
def home_riwayat(request):
    if not (is_manager(request)):
        return render(request, 'error/403.html')
    
    employee = Employee.objects.get(user=request.user)
    gedung = employee.id_gedung

    context = {
        "gedung": gedung
    }
    return render(request, "home_riwayat.html", context)

@login_required(login_url='/login/')
def list_riwayat_penjualan(request):
    if not (is_manager(request)):
        return render(request, 'error/403.html')
    
    riwayat_penjualan = []
    if (request.method == 'POST'):
        file = request.FILES['pos_file'].read().decode("utf-8").split("\n")
        for i in range(1, len(file)-1):          
            line = file[i].split(",")
            print(line)
            penjualan = POS_Penjualan(line[2],line[3],line[4],line[1])
            riwayat_penjualan.append(penjualan)
    
    response = {'riwayat_penjualan':riwayat_penjualan}
    return render(request, 'list_riwayat_penjualan.html', response)
