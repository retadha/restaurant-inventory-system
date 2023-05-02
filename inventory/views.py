from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from employee.models import Employee
from .models import Inventory
from django.contrib.auth.decorators import login_required
from propensi.utils import is_restoran, is_manager, is_staff

@login_required(login_url='/login/')
def list_inventory(request):
    if (not is_manager(request) and not is_staff(request)):
        return render(request, 'error/403.html')
    gedung = request.user.employee.id_gedung
    inventory = Inventory.objects.all().filter(id_gedung__exact=gedung)
    data = {
        'title':"Inventory",
        'inventory': inventory,
    }
    return render(request, 'inventory/list_inventory.html', data)

def update_stok(request,id):
    inventori = Inventory.objects.get(id_inventory=id)
    if(request.POST):
        inventori.stok = request.POST['stok']
        inventori.save()
        messages.success(request, f'Stok untuk inventori {inventori.default.nama} berhasil diperbarui.')
        return redirect("/inventory/")
    return render(request, 'list_inventori.html', {'inventori':inventori})

def update_threshold(request,id):
    inventori = Inventory.objects.get(id_inventory=id)
    if(request.POST):
        inventori.threshold = request.POST['threshold']
        inventori.save()
        messages.success(request, f'Ambang batas stok untuk inventori {inventori.default.nama} berhasil diperbarui.')
        return redirect("/inventory/")
    return render(request, 'list_inventori.html', {'inventori':inventori})