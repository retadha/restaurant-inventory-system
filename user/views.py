from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def create_user(request):
    # 
    return render(request, 'user/user.html')