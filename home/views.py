from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from employee.models import Employee
from gedung.models import Gedung

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def index(request):
    return render(request, 'home/home.html', {'title': "Home"})

@login_required
def profile_view(request):
    profile = Employee.objects.get(user=request.user)
    gedung = Gedung.objects.all()
    context = {
        'title': "Profil " + profile.user.username,
        'profile': profile,
        'username':profile.user.username.replace(".",""),
        'gedungs': gedung,
    }
    template = 'home/profile.html'  
    return render(request, template, context)

@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        email = request.POST['email']
        nohp = request.POST['nohp']
        try:
            employee = Employee.objects.get(user=request.user)
            employee.email = email
            employee.nohp = nohp
            employee.save()
            messages.success(request, f'Data diri berhasil diperbarui')
            return redirect('profile')
        except:
            messages.error(request, f'Data diri gagal diperbarui')
            return redirect('profile')
    
    employee = Employee.objects.get(user=request.user)
    gedung = Gedung.objects.all()
    context = {
        'title': "Edit Profile",
        'employee': employee,
        'gedung': gedung,
    }
    return render(request, 'profile.html', context)


