
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from employee.models import Employee

from .models import Inventory
from django.contrib.auth.decorators import login_required
from propensi.utils import is_restoran

def update_stok(request,id):
    inventori = Inventory.objects.get(id_inventory=id)
    if(request.POST):
        inventori.stok = request.POST['stok']
        inventori.save()
        messages.success(request, f'Stok untuk inventori {inventori.nama} berhasil diperbarui.')
        # Ganti redirect nya ke list inventori ketika sudah ada
        return redirect("/inventori/")
    return render(request, 'list_inventori.html', {'inventori':inventori})

def update_threshold(request,id):
    inventori = Inventory.objects.get(id_inventory=id)
    if(request.POST):
        inventori.threshold = request.POST['threshold']
        inventori.save()
        messages.success(request, f'Ambang batas stok untuk inventori {inventori.nama} berhasil diperbarui.')
        # Ganti redirect nya ke list inventori ketika sudah ada
        return redirect("/inventori/")
    return render(request, 'list_inventori.html', {'inventori':inventori})