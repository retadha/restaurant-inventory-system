from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gedung.models import Gedung
from propensi.utils import is_admin
from django.contrib import messages
from inventory_default.models import InventoryDefault
from inventory.models import Inventory


@login_required(login_url='/login/')
def list_gedung(request):
    if (not is_admin(request)):
        return render(request, 'error/403.html')

    gedung = Gedung.objects.all()
    context = {
        'title': "Daftar Gedung",
        "gedung": gedung,
    }
    return render(request, 'gedung_list.html', context)

@login_required(login_url='/login/')
def create_gedung(request):
    if (not is_admin(request)):
        return render(request, 'error/403.html')
    
    if request.method == 'POST':
        body = request.POST
        nama = body['nama']
        alamat = body['alamat']
        status = body['status']
        try:
            new_gedung = Gedung.objects.create(
                nama=nama,
                alamat=alamat,
                status=status,
            )
            new_gedung.save()

            inventory_def = InventoryDefault.objects.all()
            for inv in inventory_def:
                Inventory.objects.create(
                    default_id = inv.id_inventory_default,
                    stok = 0,
                    threshold = 0,
                    default_request_qty = 0,
                    id_gedung = new_gedung,
                )
            
            messages.success(request, f'Data Gedung {nama} berhasil ditambahkan')
        except:
            messages.error(request, f'Error')

    return redirect('/gedung/')

@login_required(login_url='/login/')
def update_gedung(request, gedung_id):
    if (not is_admin(request)):
        return render(request, 'error/403.html')
    
    if request.method == 'POST':
        body = request.POST
        nama = body['nama']
        alamat = body['alamat']
        status = body['status']
        try:
            print(Gedung.objects.get(id_gedung=gedung_id))
            updated_gedung = Gedung.objects.get(id_gedung=gedung_id)
            updated_gedung.nama = nama
            updated_gedung.alamat = alamat
            updated_gedung.status = status
            updated_gedung.save()
            messages.success(request, f'Gedung {nama} berhasil diperbarui')
        except:
            print("ERROR")
            messages.error(request, f'Error')

    return redirect('/gedung/')

@login_required(login_url='/login/')
def delete_gedung(request, gedung_id):
    if (not is_admin(request)):
        return render(request, 'error/403.html')

    gedung = Gedung.objects.get(id_gedung=gedung_id)
    gedung.delete()
    return redirect('/gedung/')