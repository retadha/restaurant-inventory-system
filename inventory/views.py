from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from employee.models import Employee
from inventory_default.models import InventoryDefault
from inventory_default.models import InventoryDefault

from .forms import InventoryForm
from .models import Inventory
from django.contrib.auth.decorators import login_required
from propensi.utils import is_restoran

@login_required(login_url='/login/')
def create_inventory(request):
    if request.method == "POST":
        add = InventoryForm(request.POST or None)
        if add.is_valid():
            emp = Employee.objects.get(user=request.user)
            idgedung = emp.id_gedung
            obj = add.save(commit=False)
            obj.id_gedung = idgedung
            
            nama = add.instance.id_inventory_default
            
            try:
                obj.save()
                messages.success(request, f'Inventori {nama} berhasil dibuat.')
                return redirect('inventory:create_inventory')
            except IntegrityError as e:
                if 'UNIQUE constraint' in str(e.args):
                    messages.error(request, f'Input gagal. Inventori {nama} sudah terdaftar.')
                    return redirect('inventory:create_inventory')
        else:
            print("Anj")
                
    else:
        add = InventoryForm()    
    
    inventory_default = InventoryDefault.objects.all()

    context = {
        'form': add,
        'inventory_default': inventory_default,
    }
    return render(request, 'create_inventory.html', context)

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