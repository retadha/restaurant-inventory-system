from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from request.models import Request,Inventory_Line
from employee.models import Employee
from propensi.utils import is_restoran
import datetime
import pywhatkit
import keyboard


# Create your views here.
@login_required(login_url='/login/')
def list(request):
    employee = Employee.objects.get(user=request.user)
    gedung = employee.id_gedung
    requests = Request.objects.filter(id_gedung=gedung)
    lines = Inventory_Line.objects.all()

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
        inv_request.received = datetime.datetime.now()
        inv_request.status = "3"
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")


    inv_request.save()
    return HttpResponseRedirect('/request/')

@login_required(login_url='/login/')
def delete(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.delete()
        return HttpResponseRedirect('/request/')

    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")