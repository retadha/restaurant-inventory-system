from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from request.models import Request, Inventory_Line
from employee.models import Employee
from propensi.utils import is_restoran, send_to_whatsapp
from gedung.models import Gedung
from supplier.models import Supplier
from inventory_default.models import InventoryDefault
import datetime
import pywhatkit
from django.contrib import messages
import string
import random

@login_required(login_url='/login/')
def list(request):
    employee = Employee.objects.get(user=request.user)
    gedung = employee.id_gedung
    requests = gedung.request_set.all()
    inventoryDefault = InventoryDefault.objects.all()
    suppliers = Supplier.objects.all()
    employees = Employee.objects.all()
    inventory_lines = Inventory_Line.objects.all()

    # gedung_pusat = Gedung.objects.get(status='0')
    # manager_gedung_pusat = Employee.objects.get(
    #     role='0', id_gedung=gedung_pusat).nama

    context = {
        "requests": requests,
        "is_restoran": is_restoran(request),
        "pic": employee.nama,
        "inventoryDefault": inventoryDefault,
        'suppliers': suppliers,
        'employees': employees,
        'inventory_lines': inventory_lines,
        # 'gedung': gedung,
        # 'manager_gedung_pusat': manager_gedung_pusat
    }
    
    # send_to_whatsapp("+6281298381730", "TEST TEST TEST")

    return render(request, 'request/list.html', context)


def lines_detail(inv_request):
    lines = """\n """
    for item in inv_request.get_lines:
        lines += f"{ item.id_inventory_default } @Rp{ item.harga } x { item.qty } { item.id_inventory_default.satuan }\n"
    return lines


def request_detail(inv_request, message=None):
    if inv_request.approved == None:
        detail = f"""
        {message}
        Request Inventory {inv_request.token}
        =================================
        Gedung : {inv_request.id_gedung}
        PIC : {inv_request.pic}
        Detail yang diproses: {lines_detail(inv_request)}
        Total Harga : {inv_request.total_price}"""
        return detail

    detail = f"""
    {message}
    Request Inventory {inv_request.token}
    =================================
    Gedung : {inv_request.id_gedung}
    PIC : {inv_request.pic}
    Dibuat : {inv_request.approved.strftime("%Y-%m-%d %H:%M")}
    Detail yang diproses: {lines_detail(inv_request)}
    Total Harga : {inv_request.total_price}
    """
    return detail


# Konfirmasi suatu request agar bisa dikirim
@login_required(login_url='/login/')
def confirm(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.approved = datetime.datetime.now()
        inv_request.status = "1"  # SUBMITTING
        inv_request.save()
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")
    # wa_supplier = inv_request.id_supplier.nohp

    # INTEGRASI WHATSAPP
    # Kalau request dari Resto, kirim WA ke Gudang Pusat
    if inv_request.id_gedung.get_status_display() == "RESTORAN":
        gudang = Gedung.objects.get(id_gedung=inv_request.id_gedung.id_gedung)
        manajer_gudang = Employee.objects.get(role='0', id_gedung=gudang)
        send_to_whatsapp(manajer_gudang.nohp, request_detail(
            inv_request, "Inventory Request Baru"))
    # Kalau request dari Gudang Pusat, kirim WA ke Supplier
    # send_to_whatsapp(wa_supplier, "Cek")
    if inv_request.id_gedung.get_status_display() == "GUDANG PUSAT":
        send_to_whatsapp(inv_request.id_supplier.nohp, request_detail(
            inv_request, "Inventory Request Baru"))

    messages.success(request, f'Request {inv_request.token} telah dikirim')
    return redirect("request:list")

# Daftar request restoran yang diterima oleh gudang


@login_required(login_url='/login/')
def to_process(request):
    requests = Request.objects.all()
    # requests = Request.objects.all().filter(id_gedung__status__exact="1").filter(status__exact="1")
    # print(requests)
    restauran_req = [req for req in requests if req.id_gedung.get_status_display(
    ) == "RESTORAN" and req.get_status_display() == "SUBMITTING"]

    context = {
        "requests": restauran_req,
    }

    return render(request, 'request/list_to_process.html', context)

# Gudang memproses request restoran


@login_required(login_url='/login/')
def process(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.status = "2"  # PROCESSING
        inv_request.save()
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")

    gedung = Gedung.objects.get(
        id_gedung=inv_request.id_gedung.id_gedung)  # Gudang Pusat
    list_inv_gudang = gedung.inventory_set.all()

    for line in inv_request.get_lines:
        inv_gudang = list_inv_gudang.get(default=line.id_inventory_default)
        inv_gudang.stok -= line.qty
        inv_gudang.save()

    # Whatsapp
    send_to_whatsapp(inv_request.pic.nohp, request_detail(
        inv_request, "Request sedang diproses oleh Gudang Pusat"))

    messages.success(request, f'Request {inv_request.token} telah diproses')
    return redirect("request:to_process")

# Gudang melakukan konfirmasi bahwa supplier bisa memproses request gudang


@login_required(login_url='/login/')
def supplier_process(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
        inv_request.status = "2"  # PROCESSING
        inv_request.save()
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")

    # kalau mau pake pywhatkit
    # send_to_whatsapp(wa_supplier, "Cek")

    messages.success(
        request, f'Request {inv_request.token} sedang diproses oleh supplier')
    return redirect("request:list")

# Konfirmasi bahwa inventory yang direquest sudah sampai


@login_required(login_url='/login/')
def receive(request, id_request):
    try:
        inv_request = Request.objects.get(pk=id_request)
    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")

    inv_request.received = datetime.datetime.now()
    inv_request.status = "3"  # COMPLETED
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
        print()

        employee = Employee.objects.get(user=request.user)
        if employee.id_gedung.get_status_display() == "GUDANG PUSAT":
            send_to_whatsapp(
                inv_request.pic.nohp, request_detail(inv_request, "Request Ditolak"))
            messages.success(
                request, f'Request {inv_request.token} telah ditolak')
            inv_request.delete()

            return redirect("request:to_process")

        inv_request.delete()

        messages.success(request, f'Request {inv_request.token} telah dihapus')
        return redirect("request:list")

    except Request.DoesNotExist:
        raise Http404("Objek tidak ditemukan")


@login_required(login_url='/login/')
def create(request):
    employee = Employee.objects.get(user=request.user)
    gedung = employee.id_gedung
    inventoryDefault = InventoryDefault.objects.all()
    suppliers = Supplier.objects.all()
    employees = Employee.objects.all()
    inventory_lines = Inventory_Line.objects.all()

    # gedung_pusat = Gedung.objects.get(status='0')
    # manager_gedung_pusat = Employee.objects.get(
    #     role='0', id_gedung=gedung_pusat).nama

    context = {
        "is_restoran": is_restoran(request),
        "pic": employee.nama,
        "inventoryDefault": inventoryDefault,
        'suppliers': suppliers,
        'employees': employees,
        'inventory_lines': inventory_lines,
        'gedung': gedung,
        # 'manager_gedung_pusat': manager_gedung_pusat
    }

    if (request.method == 'POST'):
        employee = Employee.objects.get(user=request.user)
        id_gedung = employee.id_gedung

        inv_request = Request.objects.create(
            pic=employee,
            id_gedung=id_gedung,
            token=''.join(random.choices(
                string.ascii_uppercase + string.digits, k=5)),
        )

        if id_gedung.status == '0':
            supplier_id = request.POST['supplier']
            supplier = Supplier.objects.get(id_supplier=supplier_id)
            inv_request.id_supplier = supplier

        inv_request.save()

        items = request.POST.getlist('item-name')
        prices = request.POST.getlist('item-price')
        quantities = request.POST.getlist('item-quantity')

        for i in range(len(items)):
            item_id = int(items[i])
            price = float(prices[i])
            quantity = int(quantities[i])

            inventory_line = Inventory_Line.objects.create(
                qty=quantity,
                harga=price,
                id_inventory_default=InventoryDefault.objects.get(
                    id_inventory_default=item_id),
                id_request=inv_request
            )
            inventory_line.save()

        messages.success(
            request, f'Request {inv_request.token} berhasil ditambahkan')

        # phone_number = "+6282170402949"
        # message = "test"
        # send_to_whatsapp(phone_number, message, 30, tab_close=True)
        return redirect("request:list")

    return render(request, 'request/create_request.html', context)


@login_required(login_url='/login/')
def update(request, id_request):
    inv_request = Request.objects.get(id_request=id_request)

    employee = Employee.objects.get(user=request.user)
    gedung = employee.id_gedung
    inventoryDefault = InventoryDefault.objects.all()
    suppliers = Supplier.objects.all()
    inventory_lines = Inventory_Line.objects.filter(id_request=inv_request)

    # gedung_pusat = Gedung.objects.get(status='0')
    # manager_gedung_pusat = Employee.objects.get(
    #     role='0', id_gedung=gedung_pusat).nama

    context = {
        "inv_request": inv_request,
        "is_restoran": is_restoran(request),
        "inventoryDefault": inventoryDefault,
        'suppliers': suppliers,
        'gedung': gedung,
        'inventory_lines': inventory_lines,
        # 'manager_gedung_pusat': manager_gedung_pusat
    }

    if (request.method == 'POST'):
        employee = Employee.objects.get(user=request.user)
        id_gedung = employee.id_gedung

        if id_gedung.status == '0':
            supplier_id = request.POST['supplier']
            supplier = Supplier.objects.get(id_supplier=supplier_id)
            inv_request.id_supplier = supplier

        inventory_lines = Inventory_Line.objects.filter(id_request=id_request)
        inventory_lines.delete()

        items = request.POST.getlist('item-name')
        prices = request.POST.getlist('item-price')
        quantities = request.POST.getlist('item-quantity')

        for i in range(len(items)):
            item_id = int(items[i])
            price = float(prices[i])
            quantity = int(quantities[i])

            inventory_line = Inventory_Line.objects.create(
                qty=quantity,
                harga=price,
                id_inventory_default=InventoryDefault.objects.get(
                    id_inventory_default=item_id),
                id_request=inv_request
            )
            inventory_line.save()

        inv_request.save()

        messages.success(
            request, f'Request {inv_request.token} berhasil diperbarui')
        employee = Employee.objects.get(user=request.user)
        if employee.id_gedung.get_status_display() == "GUDANG PUSAT":
            return redirect("request:to_process")

        return redirect("request:list")

    return render(request, 'request/update_request.html', context)
