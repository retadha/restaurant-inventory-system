from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from inventory_default.models import InventoryDefault
from .forms import InventoryDefaultForm
from django.contrib.auth.decorators import login_required
from propensi.utils import is_restoran, is_manager, is_staff


@login_required(login_url='/login/')
def list_inventory_default(request):
    statGedung = request.user.employee.id_gedung.status

    if (not is_manager(request) or statGedung != '0'):
        return render(request, 'error/403.html')
    inventory_def = InventoryDefault.objects.all()
    data = {
        'title': "List Inventory Default",
        "inventory": inventory_def,
    }
    return render(request, 'list_inventory_default.html', data)


@login_required(login_url='/login/')
def create_inventory_default(request):
    if request.method == "POST":
        add = InventoryDefaultForm(request.POST or None)
        if add.is_valid():
            add.save()
            messages.success(
                request, f'Inventori {add.instance.nama} berhasil dibuat.')
            return redirect('inventory_default:list_inventory_default')
        else:
            messages.error(
                request, f'Input gagal. Inventori {add.instance.nama} sudah terdaftar.')
            return redirect('inventory_default:list_inventory_default')

    add = InventoryDefaultForm()
    return render(request, 'create_inventory_default.html', {'form': add})


@login_required(login_url='/login/')
def delete(request, id_inventory_default):
    try:
        inv = InventoryDefault.objects.get(pk=id_inventory_default)
        messages.success(request, f'Inventori {inv.nama} berhasil dihapus.')
        inv.delete()
        return HttpResponseRedirect('/inventory_default')
    except InventoryDefault.DoesNotExist:
        raise Http404("Objek tidak ditemukan")
