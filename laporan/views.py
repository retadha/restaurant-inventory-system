from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from request.models import Request, Inventory_Line
from inventory.models import Inventory
from propensi.utils import is_manager
from django.contrib.auth.decorators import login_required
from django.db.models import Sum



@login_required(login_url='/login/')
def pembelian(request):
    statGedung = request.user.employee.id_gedung.status
    gedung = request.user.employee.id_gedung

    if (not is_manager(request) or statGedung !='0'):
        return render(request, 'error/403.html')
    inventory = Inventory.objects.all().filter(id_gedung__exact=gedung)
    
    wait = waited_orders(self=request)
    submit = submitted_orders(self=request)
    process = processed_orders(self=request)
    complete = completed_orders(self=request)
    quantityTBR = quantity_TBR(request)
    total = total_purchase(self=request)
    
    totalStok = inventory.aggregate(Sum('stok')).get('stok__sum')
    context = {
        'title': "Laporan Pembelian",
        'totalStok': totalStok,
        'wait' : wait,
        'submit' : submit,
        'process': process,
        'complete' : complete,
        'quantityTBR' : quantityTBR,
        'total' : total,
    }
    template = 'laporan/pembelian.html'  
    return render(request, template, context)

def waited_orders(self, queryset=None):
    obj = Request.objects.filter(status__exact="0")
    count = len(obj)
    return count

def submitted_orders(self, queryset=None):
    obj = Request.objects.filter(status__exact="1")
    count = len(obj)
    return count

def processed_orders(self, queryset=None):
    obj = Request.objects.filter(status__exact="2")
    count = len(obj)
    return count

def completed_orders(self, queryset=None):
    obj = Request.objects.filter(status__exact="3")
    count = len(obj)
    return count

def quantity_TBR(self, queryset=None):
    obj = Request.objects.filter(status__exact="2").values_list('id_request')
    jumlah = 0
    for i in obj:
        stok = Inventory_Line.objects.filter(id_request__exact=i).aggregate(Sum('qty'))['qty__sum']
        jumlah += stok
    
    if jumlah == None:
        jumlah = 0
            
    return jumlah

def total_purchase(self, queryset=None):
    obj = Request.objects.filter(status='2') | Request.objects.filter(status='3')
    total = 0
    for i in obj:
        query = Inventory_Line.objects.filter(id_request__exact=i)
        
        for a in query:
            price = a.qty * a.harga
            total+= price
            
        if total == None:
            total= 0
    return total
