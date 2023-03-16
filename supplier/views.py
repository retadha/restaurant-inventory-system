from django.shortcuts import render, redirect
from .forms import AddSupplierForm
from .models import Supplier

# Create your views here.
def create_supplier(request):
    context = {}
    form = AddSupplierForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()  
    context['form']= form
    return render(request, "add_supplier_form.html", context)


def list_supplier(request):
    suppliers = Supplier.objects.all()
    response = {'suppliers':suppliers}
    return render(request, 'list_supplier.html', response)
