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
    status = "PROCESSING"
    if (not is_manager(request) or statGedung !='0'):
        return render(request, 'error/403.html')
    inventory = Inventory.objects.all().filter(id_gedung__exact=gedung)
    # request = Request.objects.all().filter(status__exact=status).values_list('status')
    
    totalStok = inventory.aggregate(Sum('stok')).get('stok__sum')
    # stokTBR = inventory
    context = {
        'title': "Laporan Pembelian",
        'totalStok': totalStok,
        # 'request':request,
    }
    template = 'laporan/pembelian.html'  
    return render(request, template, context)

