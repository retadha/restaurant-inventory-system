from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ResepForm
from .models import Resep
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def create_resep(request):
    if request.method == "POST":
        add = ResepForm(request.POST)
        if add.is_valid():
            namaResep = add.cleaned_data.get('nama')
            add.save()
        messages.success(request, f'Resep {namaResep} berhasil dibuat.')
        return redirect("resep:viewall_resep")
    add = ResepForm()
    return render(request, 'create.html', {'form':add})

@login_required(login_url='/login/')
def viewall_resep(request):
    daftar_resep = Resep.objects.all()
    context = {
        "daftar_resep" : daftar_resep
    }
    return render(request, 'viewall_resep.html', context)

@login_required(login_url='/login/')
def view_resep(request, id_resep):
    resep = Resep.objects.get(pk=id_resep)
    context = {
        "id_resep" : resep.id_resep,
        "nama" : resep.nama,
        "bahan" : resep.bahan,
        "cara_memasak" : resep.cara_memasak
    }
    return render(request, 'view_resep.html', context)

@login_required(login_url='/login/')
def edit_resep(request, id_resep):
    try:
        resep = Resep.objects.get(pk=id_resep)
    except Resep.DoesNotExist:
        raise Http404("Objek tidak ditemukan")

    if request.method == "POST":
        resep = Resep.objects.get(pk=id_resep)
        resep.nama = request.POST["nama"]
        resep.bahan = request.POST["bahan"]
        resep.cara_memasak = request.POST["cara_memasak"]
        resep.save()
        messages.success(request, f'Resep {resep.nama} berhasil diubah.')
        return HttpResponseRedirect('/resep/viewall')

    context = {
        'id_resep' : resep.id_resep,
        'nama' : resep.nama,
        'bahan' : resep.bahan,
        'cara_memasak' : resep.cara_memasak

    }
    return render(request, "update_resep.html", context)

@login_required(login_url='/login/')
def delete_resep(request, id_resep):
    try:
        resep = Resep.objects.get(pk=id_resep)
        resep.delete()
        return HttpResponseRedirect('/resep/viewall')
    except Resep.DoesNotExist:
        raise Http404("Objek tidak ditemukan")