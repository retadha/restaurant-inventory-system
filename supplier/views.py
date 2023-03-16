from django.shortcuts import render, redirect
from .forms import AddSupplierForm
from .models import Supplier

# Create your views here.
def create_supplier(request):
    if request.method == "POST":
        add = AddSupplierForm(request.POST)
        if add.is_valid():
            add.save()
        return redirect("supplier:create_supplier")
    add = AddSupplierForm()     
    return render(request, 'supplier/create_supplier.html', {'form':add})

def list_supplier(request):
    suppliers = Supplier.objects.all()
    response = {'supplier':suppliers}
    return render(request, 'supplier/list_supplier.html', response)
