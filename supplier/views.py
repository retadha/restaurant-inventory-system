from django.shortcuts import render, redirect
from .models import Supplier

# Create your views here.
def create_supplier(request):
    if(request.POST):
        supplier = Supplier.objects.create()
        supplier.nama = request.POST["nama"]
        supplier.alamat = request.POST["alamat"]
        supplier.pic = request.POST["pic"]
        supplier.nohp = request.POST["nohp"]
        supplier.save()
        return redirect("/supplier/list_supplier")
    return render(request, 'add_supplier_form.html')

def list_supplier(request):
    suppliers = Supplier.objects.all()
    response = {'suppliers':suppliers}
    return render(request, 'list_supplier.html', response)

def update_supplier(request,id):
    supplier = Supplier.objects.get(id_supplier=id)
    if(request.POST):
        supplier.nama = request.POST["nama"]
        supplier.alamat = request.POST["alamat"]
        supplier.pic = request.POST["pic"]
        supplier.nohp = request.POST["nohp"]
        supplier.save()
        return redirect("/supplier/list_supplier")
    return render(request, 'list_supplier.html', {'supplier':supplier})

def get_supplier(request,id):
        supplier = Supplier.objects.get(id_supplier=id)  
        return render(request,'list_supplier.html', {'supplier':supplier})

def delete_supplier(request,id):
    supplier = Supplier.objects.get(id_supplier=id)
    supplier.delete()
    return redirect("/supplier/list_supplier")