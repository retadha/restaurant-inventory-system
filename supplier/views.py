from django.shortcuts import render, redirect
from .models import Supplier
from django.contrib import messages
from propensi.utils import is_gudang_pusat, is_manager, is_staff

# Create your views here.
def create_supplier(request):
    if(auth_gedung_pusat(request) == False):
        return render(request, 'error/403.html')
    if(request.POST):
        supplier = Supplier.objects.create()
        supplier.nama = request.POST["nama"]
        supplier.alamat = request.POST["alamat"]
        supplier.pic = request.POST["pic"]
        supplier.nohp = request.POST["nohp"]
        supplier.save()
        messages.success(request, f'Supplier {supplier.nama} berhasil ditambahkan.')
        return redirect("/supplier/")
    return render(request, 'list_supplier_datatables.html')

def list_supplier(request):
    print(auth_gedung_pusat(request))
    if(auth_gedung_pusat(request) == False):
        return render(request, 'error/403.html')
    suppliers = Supplier.objects.all()
    response = {'suppliers':suppliers}
    return render(request, 'list_supplier_datatables.html', response)

def update_supplier(request,id):
    if(auth_gedung_pusat(request) == False):
        return render(request, 'error/403.html')
    supplier = Supplier.objects.get(id_supplier=id)
    if(request.POST):
        supplier.nama = request.POST["nama"]
        supplier.alamat = request.POST["alamat"]
        supplier.pic = request.POST["pic"]
        supplier.nohp = request.POST["nohp"]
        supplier.save()
        messages.success(request, f'Supplier {supplier.nama} berhasil diubah.')
        return redirect("/supplier/")
    return render(request, 'list_supplier_datatables.html', {'supplier':supplier})

def get_supplier(request,id):
    if(auth_gedung_pusat(request) == False):
        return render(request, 'error/403.html')
    supplier = Supplier.objects.get(id_supplier=id)  
    return render(request,'list_supplier_datatables.html', {'supplier':supplier})

def delete_supplier(request,id):
    if(auth_gedung_pusat(request) == False):
        return render(request, 'error/403.html')
    supplier = Supplier.objects.get(id_supplier=id)
    supplier.delete()
    return redirect("/supplier/")

def auth_gedung_pusat(request):
    if (is_manager(request) | is_staff(request)):
        if (is_gudang_pusat(request)):
            return True
        return False
    return False