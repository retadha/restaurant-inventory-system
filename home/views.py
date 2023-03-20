from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from employee.models import Employee
from .forms import UserUpdateForm


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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
    
        if u_form.is_valid():
            u_form.save()
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }

    return render(request, 'home/profile.html', context)
