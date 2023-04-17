from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages

from inventory_default.models import InventoryDefault

from .forms import InventoryDefaultForm
from django.contrib.auth.decorators import login_required
from propensi.utils import is_restoran

@login_required(login_url='/login/')
def create_inventory_default(request):
    if request.method == "POST":
        add = InventoryDefaultForm(request.POST or None)
        if add.is_valid():
            add.save()
            messages.success(request, f'Inventori {add.instance.nama} berhasil dibuat.')
            return redirect('inventory_default:create_inventory_default')
        else:
                messages.error(request, f'Input gagal. Inventori {add.instance.nama} sudah terdaftar.')
                return redirect('inventory_default:create_inventory_default')
        
    add = InventoryDefaultForm()
    return render(request, 'create_inventory_default.html', {'form':add})

@login_required(login_url='/login/')
def delete(request, id_inventory_default):
    try:
        inv = InventoryDefault.objects.get(pk=id_inventory_default)
        inv.delete()
        return HttpResponseRedirect('/inventory_default/create')
    except InventoryDefault.DoesNotExist:
        raise Http404("Objek tidak ditemukan")