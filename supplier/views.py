from django.shortcuts import render, redirect
from .forms import AddSupplierForm
from .models import Supplier

# Create your views here.
def create_supplier(request):
    context = {}
    form = AddSupplierForm(request.POST)
    if form.is_valid():
        form.save()  
    context['form']= form
    return render(request, "add_supplier_form.html", context)

def list_supplier(request):
    suppliers = Supplier.objects.all()
    response = {'suppliers':suppliers}
    return render(request, 'list_supplier.html', response)

def update_supplier(request,id):
    supplier = Supplier.objects.get(id=id)
    form = AddSupplierForm(request.POST, instance=supplier)
    if form.is_valid():  
        form.save()
    return render(request, 'update_supplier.html', supplier)

def get_supplier(request,id):
        supplier = Supplier.objects.get(id=id)  
        return render(request,'get_supplier.html', {'supplier':supplier})

def delete_supplier(request,id):
    supplier = Supplier.objects.get(id=id)
    supplier.delete()
    return redirect("/list_supplier")