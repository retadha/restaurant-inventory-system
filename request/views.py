from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from request.models import Request,Inventory_Line
from inventory.models import Inventory
from employee.models import Employee
from propensi.utils import is_restoran
from gedung.models import Gedung
import datetime
import pywhatkit
import keyboard


# Create your views here.
@login_required(login_url='/login/')
def list(request):
    employee = Employee.objects.get(user=request.user)
    gedung = employee.id_gedung
    requests = gedung.request_set.all()

    context = {
        "requests" : requests,
        "is_restoran" : is_restoran(request),
    }

    return render(request, 'request/list.html', context)

@login_required(login_url='/login/')
def accept(request):
    requests = Request.objects.filter()

    context = {
        "requests" : requests,
        "is_restoran" : is_restoran(request),
    }

    return render(request, 'request/list.html', context)

@login_required(login_url='/login/')
def confirm(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.created = datetime.datetime.now()
        inv_request.status = "1"
        inv_request.save()
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")
    wa_supplier = inv_request.id_supplier.nohp

    # kalau mau pake pywhatkit
    # pywhatkit.sendwhatmsg_instantly(wa_supplier, "Cek")

    return HttpResponseRedirect('/request/')

@login_required(login_url='/login/')
def receive(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")

    inv_request.received = datetime.datetime.now()
    inv_request.status = "3"
    inv_request.save()

    gedung = inv_request.id_gedung
    list_inventori_gedung = gedung.inventory_set.all()

    for line in inv_request.get_lines:
        inv_gedung = list_inventori_gedung.get(default=line.id_inventory_default)
        inv_gedung.stok += line.qty
        inv_gedung.save()


    return HttpResponseRedirect('/request/')

@login_required(login_url='/login/')
def delete(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.delete()
        return HttpResponseRedirect('/request/')

    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")