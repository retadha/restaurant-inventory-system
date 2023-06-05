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
        'title': "Daftar Inventory",
        'inventory': inventory,
    }
    return render(request, 'inventory/list_inventory.html', data)


@login_required(login_url='/login/')
def update_stok(request, id):
    if (not is_manager(request) and not is_staff(request)):
        return render(request, 'error/403.html')
    inventori = Inventory.objects.get(id_inventory=id)
    if (request.POST):
        inventori.stok = request.POST['stok']
        inventori.save()
        messages.success(
            request, f'Stok untuk inventori {inventori.default.nama} berhasil diperbarui.')
        return redirect("/inventory/")
    return render(request, 'list_inventori.html', {'inventori': inventori})


@login_required(login_url='/login/')
def update_threshold(request, id):
    if (not is_manager(request) and not is_staff(request)):
        return render(request, 'error/403.html')
    inventori = Inventory.objects.get(id_inventory=id)
    if (request.POST):
        inventori.threshold = request.POST['threshold']
        inventori.save()
        messages.success(
            request, f'Ambang batas stok untuk inventori {inventori.default.nama} berhasil diperbarui.')
        return redirect("/inventory/")
    return render(request, 'list_inventori.html', {'inventori': inventori})


@login_required(login_url='/login/')
def update_pos(request):
    employee = request.user.employee
    gedung = employee.id_gedung
    if (request.method == 'POST'):
        file = request.FILES['pos_file'].read().decode("utf-8").split("\n")
        data = []
        for i in range(1, len(file)):
            line = file[i].split(",")
            # print(line)
            data.append({
                "id": line[0],
                'date':line[1],
                'product': line[2],
                "total": int(line[3]),
                "price": int(line[4]),
                'notes': line[5],
            })
        # print(data)
        for i in data:
            inventory = Inventory.objects.filter(id_gedung__exact=gedung).filter(
                default__nama__exact=i['product'])
            if (len(inventory) != 0):
                inventory = inventory[0]
                # print(inventory)
                inventory.stok = inventory.stok - i['total']
                if (inventory.threshold > inventory.stok):
                    # print("warning")
                    messages.warning(request, 
                                     f'Stok inventory {inventory.default.nama} sudah di bawah ambang batas.')
                inventory.save()
    return redirect("/inventory/")
