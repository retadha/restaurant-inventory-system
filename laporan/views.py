from decimal import Decimal
import simplejson as json
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from propensi.utils import is_manager, is_restoran
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, ExtractMonth
from inventory_default.models import InventoryDefault
from inventory.models import Inventory
from supplier.models import Supplier
from request.models import Request, Inventory_Line
import datetime


@login_required(login_url='/login/')
def index(request):
    if (not is_manager(request)):
        return render(request, 'error/403.html')

    context = {
        'title': "Laporan"
    }

    return render(request, 'laporan/index.html', context)


@login_required(login_url='/login/')
def pembelian(request):
    statGedung = request.user.employee.id_gedung.status
    gedung = request.user.employee.id_gedung
    last = Request.objects.latest('approved').approved
    tahun = datetime.date.today().year

    if (not is_manager(request) or statGedung != '0'):
        return render(request, 'error/403.html')
    inventory = Inventory.objects.all().filter(id_gedung__exact=gedung)

    wait = waited_orders(self=request)
    submit = submitted_orders(self=request)
    process = processed_orders(self=request)
    complete = completed_orders(self=request)
    quantityTBR = quantity_TBR(request)
    total = total_purchase(self=request)
    sup = top_supplier(self=request)
    item = top_item(self=request)
    month = per_month_purchase(self=request)
    items = per_month_items(self=request)

    
    totalStok = inventory.aggregate(Sum('stok')).get('stok__sum')
    context = {
        'title': "Laporan Pembelian " + gedung.nama,
        'totalStok': totalStok,
        'wait': wait,
        'submit': submit,
        'process': process,
        'complete': complete,
        'quantityTBR': quantityTBR,
        'total': total,
        'sup': sup,
        'item': item,
        'month': month,
        'items' : items,
        'last' : last,
        'tahun' : tahun,
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
    
    # <!--Menghitung total quantity berdasarkan request yang berstatus processing-->
    for i in obj:
        stok = Inventory_Line.objects.filter(id_request__exact=i).aggregate(Sum('qty'))['qty__sum']
        jumlah += stok

    if jumlah == None:
        jumlah = 0

    return jumlah


def total_purchase(self, queryset=None):
    obj = Request.objects.filter(
        status='2') | Request.objects.filter(status='3')
    total = 0
    
    # <!--Menghitung total harga berdasarkan request yang berstatus processing & completed-->
    for i in obj:
        query = Inventory_Line.objects.filter(id_request__exact=i)

        for a in query:
            price = a.qty * a.harga
            total += price

        if total == None:
            total = 0
    return total


def top_item(self, queryset=None):
    query = Request.objects.filter(status='2') | Request.objects.filter(status='3')
    
    qty_dict = dict()
    for i in query:
        obj = Inventory_Line.objects.filter(id_request__exact=i)
        
        for a in obj:
            nama = a.id_inventory_default.nama
            qt = a.qty
            
            # <!--Mapping untuk setiap nama inventory dan jumlahnya-->
            if nama in qty_dict.keys():
                qty_dict[nama] = qty_dict[nama] + qt
            else:
                qty_dict.update({nama: qt})
                
                
    max_value = max(qty_dict.values())
    item = [k for k,v in qty_dict.items() if v == max_value]
          
    return ", ".join(item) 


def top_supplier(self, queryset=None):
    query = Request.objects.filter(status='2') | Request.objects.filter(status='3')
    
    qty_dict = dict()
    for i in query:
        if (i.id_gedung.status == "0"):
            namaSupplier = i.id_supplier.nama
            
            if namaSupplier in qty_dict.keys():
                    qty_dict[namaSupplier] = qty_dict[namaSupplier] + 1
            else:
                qty_dict.update({namaSupplier: 1})
        
    max_value = max(qty_dict.values())
    item = [k for k,v in qty_dict.items() if v == max_value]
          
    return ", ".join(item)


def per_month_purchase(self, queryset=None):
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    tahun = datetime.date.today().year
    
    obj = Request.objects.filter(approved__year = tahun).annotate(month=ExtractMonth('approved')).values(
        'month').annotate(c=Count('id_request')).values('month', 'c')

    for i in range(0, 12):
        for a in obj:
            if a['month'] == i:
                obj2 = Request.objects.filter(approved__year = tahun, approved__month=i)
                total = 0
                for x in obj2:
                    query = Inventory_Line.objects.filter(id_request__exact=x)

                    for y in query:
                        price = y.qty * y.harga
                        total += price

                    if total == None:
                        total = 0
                arr[i-1] = total
            else:
                pass
    arrResult = json.dumps(arr)

    return arrResult

def per_month_items(self, queryset=None):
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    tahun = datetime.date.today().year
    
    obj = Request.objects.filter(approved__year = tahun).annotate(month=ExtractMonth('approved')).values(
        'month').annotate(c=Count('id_request')).values('month', 'c')

    for i in range(0, 12):
        for a in obj:
            if a['month'] == i:
                obj2 = Request.objects.filter(approved__year = tahun, approved__month=i)
                total = 0
                for x in obj2:
                    query = Inventory_Line.objects.filter(id_request__exact=x)

                    for y in query:
                        jumlah = y.qty 
                        total += jumlah

                    if total == None:
                        total = 0
                arr[i-1] = total
            else:
                pass
    arrResult = json.dumps(arr)

    return arrResult


@login_required(login_url='/login/')
def penjualan(request):
    gedung = request.user.employee.id_gedung

    if (not is_manager(request) or not is_restoran(request)):
        return render(request, 'error/403.html')

    context = {
        'title': "Laporan Penjualan " + gedung.nama,
    }

    if (request.method == 'POST'):
        file = request.FILES['pos_file'].read().decode("utf-8").split("\n")
        data = []
        for i in range(1, len(file)):
            line = file[i].split(",")
            # print(line)
            data.append({
                "id": line[0],
                'date': line[1],
                'product': line[2],
                "total": int(line[3]),
                "price": int(line[4]),
                'notes': line[5],
            })
        # print(data)

        product = ""
        max_product = 0
        itemCount = {}
        total = 0
        price = 0
        monthCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in data:
            if (i['product'] in itemCount):
                itemCount[i['product']]['count'] += 1
            else:
                itemCount[i['product']] = {'product': i['product'], 'count': 1}

            dateList = i['date'].split("/")
            # print(dateList)
            date = datetime.datetime(
                int(dateList[2]), int(dateList[0]), int(dateList[1]))
            monthCount[int(date.strftime("%m")) - 1] += i['price']
            total += i['total']
            price += i['price']
        # print(itemCount)
        for i in itemCount:
            # print(itemCount[i]['count'])
            if (itemCount[i]['count'] > max_product):
                product = i
                max_product = itemCount[i]['count']
            elif (product == ""):
                product = i
                max_product = itemCount[i]['count']

        context['product'] = product
        context['total'] = total
        context['price'] = price
        context['month'] = monthCount

    return render(request, 'laporan/penjualan.html', context)
