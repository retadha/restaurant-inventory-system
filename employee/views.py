from django.shortcuts import render, redirect
from .models import Employee
from gedung.models import Gedung
from .forms import EmployeeCreationForm
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
            nama = form.cleaned_data.get('nama')
            messages.success(request, f'Karyawan {nama} berhasil ditambahkan')
            return redirect('employee_list')
        else:
            # for field_name, errors in form.errors.items():
            #     for error in errors:
            #         messages.error(request, f'{error}')
            # print(form.errors.items())
            messages.error(request, f'Error')
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm()

    gedung = Gedung.objects.all()

    context = {
        'title': "Buat Employee",
        'form': form,
        'gedung': gedung,
    }
    return render(request, 'create_employee.html', context)


@login_required(login_url='/login/')
def employee_list(request):
    if (is_admin(request) == False):
        return render(request, 'error/403.html')
    
    employees = Employee.objects.all()
    gedung = Gedung.objects.all()
    
    context = {
        'title': "Daftar Employee",
        'employees': employees,
        'gedung': gedung,
    }
    return render(request, 'employee_list.html', context)


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
            employee = Employee.objects.get(id=employee_id)
            employee.user.username = username
            employee.user.email = email
            employee.nama = nama
            employee.role = role
            employee.nohp = phone
            employee.id_gedung = Gedung.objects.get(pk=gd)
            employee.save()

            if (len(pwd) != 0):
                if (pwd == confirmPwd):
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    messages.success(
                        request, f'Data Karyawan {nama} berhasil diperbarui')
                else:
                    messages.error(request, f'Password tidak sama')
            else:
                messages.success(
                    request, f'Data Karyawan {nama} berhasil diperbarui')
            return redirect('employee_list')
        except:
            messages.error(request, f'Error')
            return redirect('employee_list')

    employee = Employee.objects.get(id=employee_id)
    gedung = Gedung.objects.all()
    context = {
        'title': "Update Employee",
        'employee': employee,
        'gedung': gedung,
    }
    return render(request, 'employee_list.html', context,)


@login_required(login_url='/login/')
def delete_employee(request, employee_id):
    if (is_admin(request) == False):
        return render(request, 'error/403.html')

    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    User.objects.get(username=employee.user.username).delete()
    return redirect('employee_list')
