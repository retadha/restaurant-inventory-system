from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User

from .forms import UserUpdateForm
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
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserUpdateForm()

    employee = Employee.objects.get(user=request.user)
    gedung = Gedung.objects.all()

    context = {
        'title': "Edit",
        'form': form,
        'employee': employee,
        'gedung': gedung,
    }
    return render(request, 'home/edit_profile.html', context)



