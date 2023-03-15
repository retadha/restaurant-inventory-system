from django.shortcuts import redirect, render
from .forms import AddResepForm

def create_resep(request):
    if request.method == "POST":
        add = AddResepForm(request.POST)
        if add.is_valid():
            add.save()
        return redirect("resep:create_resep")
    add = AddResepForm()     
    return render(request, 'resep/create.html', {'form':add})