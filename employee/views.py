from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

def is_admin(user):
    return user.is_authenticated and Employee.objects.get(user=user).role == 'ADMIN'

@user_passes_test(is_admin)
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm()
    return render(request, 'create_employee.html', {'form': form})

@user_passes_test(is_admin)
def employee_list(request):
    query = request.GET.get('search-area', '')
    employees = Employee.objects.filter(
        Q(nama__icontains=query) |
        Q(email__icontains=query) |
        Q(role__icontains=query) |
        Q(id_gedung__nama__icontains=query)
        )
    return render(request, 'employee_list.html', {'employees': employees})

@user_passes_test(is_admin)
def employee_detail(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
   
    return render(request, 'employee_detail.html', {'employee': employee})