from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from request.models import Request,Inventory_Line
from employee.models import Employee
from propensi.utils import is_restoran
import datetime


# Create your views here.
# @login_required(login_url='/login/')
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

def confirm(request, id_request):
    inv_request = Request.objects.get(pk=id_request)
    inv_request.created = datetime.datetime.now()
    inv_request.status = "1"
    inv_request.save()
    return HttpResponseRedirect('/request/')

def receive(request, id_request):
    inv_request = Request.objects.get(pk=id_request)
    inv_request.received = datetime.datetime.now()
    inv_request.status = "3"
    inv_request.save()
    return HttpResponseRedirect('/request/')