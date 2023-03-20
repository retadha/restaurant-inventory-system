from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User

from employee.models import Employee
from gedung.models import Gedung

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def index(request):
    return render(request, 'home/home.html', {'title': "Home"})

@login_required
def profile_view(request):
    profile = Employee.objects.get(user=request.user)
    context = {
        'profile': profile
    }
    template = 'home/profile.html'  
    return render(request, template, context)

@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        body = request.POST
        username = body['username']
        nama = body['nama']
        email = body['email']
        role = body['role']
        gd = body['gedung']
        phone = body['phone']
        try:
            employee = Employee.objects.get(user=request.user)
            employee.user.username = username
            employee.user.email = email
            employee.nama = nama
            employee.role = role
            employee.nohp = phone
            employee.id_gedung = Gedung.objects.get(pk=gd)
            employee.save()
            messages.success(request, f'Berhasil diperbarui')
            return redirect('home')
        except:
            messages.error(request, f'Error')

    employee = Employee.objects.get(user=request.user)
    gedung = Gedung.objects.all()
    context = {
        'title': "Update Profile", 
        'employee': employee,
        'gedung':gedung,
    }
    return render(request, 'home/edit_profile.html', context,)