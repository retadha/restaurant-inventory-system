from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import ResepForm
from .models import Resep


def create_resep(request):
    if request.method == "POST":
        add = ResepForm(request.POST)
        if add.is_valid():
            add.save()
        return redirect("resep:create_resep")
    add = ResepForm()
    return render(request, 'resep/templates/create.html', {'form':add})

def viewall_resep(request):
    daftar_resep = Resep.objects.all()
    context = {
        "daftar_resep" : daftar_resep
    }
    return render(request, 'viewall_resep.html', context)

def view_resep(request, id_resep):
    resep = Resep.objects.get(pk=id_resep)
    context = {
        "id_resep" : resep.id_resep,
        "nama" : resep.nama,
        "bahan" : resep.bahan,
        "cara_memasak" : resep.cara_memasak
    }
    return render(request, 'view_resep.html', context)

def edit_resep(request, id_resep):
    try:
        resep = Resep.objects.get(pk=id_resep)
    except Resep.DoesNotExist:
        raise Http404("Objek tidak ditemukan")
    form = ResepForm(request.POST or None, instance= resep)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/resep/viewall')

    context = {
        'id_resep' : resep.id_resep,
        'form' : form
    }
    return render(request, "update_resep.html", context)

def delete_resep(request, id_resep):
    try:
        resep = Resep.objects.get(pk=id_resep)
        resep.delete()
        return HttpResponseRedirect('/resep/viewall')
    except Resep.DoesNotExist:
        raise Http404("Objek tidak ditemukan")




