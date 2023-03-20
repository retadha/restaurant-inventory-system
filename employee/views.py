from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeCreationForm
from django.db.models import Q
from propensi.utils import is_admin
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def create_employee(request):
    if (is_admin(request) == False):
        return render(request, 'error/403.html')
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm()
    return render(request, 'create_employee.html', {'title': "Buat Employee", 'form': form})

@login_required(login_url='/login/')
def employee_list(request):
    if (is_admin(request) == False):
        return render(request, 'error/403.html')
    query = request.GET.get('search-area', '')
    employees = Employee.objects.filter(
        Q(nama__icontains=query) |
        Q(email__icontains=query) |
        Q(role__icontains=query) |
        Q(id_gedung__nama__icontains=query)
    )
    return render(request, 'employee_list.html', {'title': "Daftar Employee", 'employees': employees})

@login_required(login_url='/login/')
def employee_detail(request, employee_id):
    if (is_admin(request) == False):
        return render(request, 'error/403.html')
    employee = Employee.objects.get(id=employee_id)
    return render(request, 'employee_detail.html', {'title': "Detail Employee", 'employee': employee})
