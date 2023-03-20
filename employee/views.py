from django.shortcuts import render, redirect
from .models import Employee
from gedung.models import Gedung
from .forms import EmployeeCreationForm
from django.db.models import Q
from propensi.utils import is_admin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

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


@login_required(login_url='/login/')
def update_employee(request, employee_id):
    if (is_admin(request) == False):
        return render(request, 'error/403.html')
    if request.method == 'POST':
        body = request.POST
        username = body['username']
        password = body['password']
        nama = body['nama']
        email = body['email']
        role = body['role']
        gd = body['gedung']
        phone = body['phone']
        pwd = body['password']
        confirmPwd = body['confirmPwd']
        try:
            if (len(pwd) == 0):
                employee = Employee.objects.get(id=employee_id)
                employee.user.username = username
                employee.user.email = email
                employee.nama = nama
                employee.role = role
                employee.nohp = phone
                employee.id_gedung = Gedung.objects.get(pk=gd)
                employee.save()
                messages.success(request, f'Karyawan {nama} berhasil diperbarui')
                return redirect('employee_list')
            else:
                if (pwd == confirmPwd):
                    pass
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    messages.success(request, f'Karyawan {nama} berhasil diperbarui')
                    return redirect('employee_list')
                else:
                    messages.error(request, f'Password tidak sama')
        except:
            messages.error(request, f'Error')

    employee = Employee.objects.get(id=employee_id)
    gedung = Gedung.objects.all()
    context = {
        'title': "Update Employee", 
        'employee': employee,
        'gedung':gedung,
    }
    return render(request, 'update_employee.html', context,)

@login_required(login_url='/login/')
def delete_employee(request, employee_id):
    if (is_admin(request) == False):
        return render(request, 'error/403.html')
    
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    User.objects.get(username=employee.user.username).delete()
    return redirect('employee_list')
