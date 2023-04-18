from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from request.models import Request,Inventory_Line
from inventory.models import Inventory
from employee.models import Employee
from propensi.utils import is_restoran
from gedung.models import Gedung
import datetime
import pywhatkit
import keyboard
from django.contrib import messages



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
def confirm(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.approved = datetime.datetime.now()
        inv_request.status = "1" # SUBMITTING
        inv_request.save()
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")
    wa_supplier = inv_request.id_supplier.nohp

    # INTEGRASI WHATSAPP
    # Kalau request dari Resto, kirim WA ke Gudang Pusat
    # Kalau request dari Gudang Pusat, kirim WA ke Supplier
    # pywhatkit.sendwhatmsg_instantly(wa_supplier, "Cek")

    messages.success(request, f'Request {inv_request.token} telah dikirim')
    return redirect("request:list")

@login_required(login_url='/login/')
def to_process(request):
    requests = Request.objects.all()
    restauran_req = [req for req in requests if req.id_gedung.get_status_display() == "RESTORAN" and req.get_status_display() == "SUBMITTING" ]

    context = {
        "requests" : restauran_req,
    }

    return render(request, 'request/list_to_process.html', context)

@login_required(login_url='/login/')
def process(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.status = "2" # PROCESSING
        inv_request.save()
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")

    gedung = Gedung.objects.get(status="0") #Gudang Pusat
    list_inv_gudang = gedung.inventory_set.all()

    for line in inv_request.get_lines:
        inv_gudang = list_inv_gudang.get(default=line.id_inventory_default)
        inv_gudang.stok -= line.qty
        inv_gudang.save()

    # kalau mau pake pywhatkit
    # pywhatkit.sendwhatmsg_instantly(wa_supplier, "Cek")

    messages.success(request, f'Request {inv_request.token} telah diproses')
    return redirect("request:to_process")

@login_required(login_url='/login/')
def supplier_process(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.status = "2" # PROCESSING
        inv_request.save()
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")

    # kalau mau pake pywhatkit
    # pywhatkit.sendwhatmsg_instantly(wa_supplier, "Cek")

    messages.success(request, f'Request {inv_request.token} sedang diproses oleh supplier')
    return redirect("request:list")


@login_required(login_url='/login/')
def receive(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")

    inv_request.received = datetime.datetime.now()
    inv_request.status = "3" #COMPLETED
    inv_request.save()

    gedung = inv_request.id_gedung
    list_inv_resto = gedung.inventory_set.all()

    for line in inv_request.get_lines:
        inv_resto = list_inv_resto.get(default=line.id_inventory_default)
        inv_resto.stok += line.qty
        inv_resto.save()

    messages.success(request, f'Request {inv_request.token} telah diterima')
    return redirect("request:list")

@login_required(login_url='/login/')
def delete(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.delete()

        messages.success(request, f'Request {inv_request.token} telah dihapus')
        return redirect("request:list")

    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")