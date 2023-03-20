from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def index(request):
    return render(request, 'home/home.html', {'title': "Home"})
