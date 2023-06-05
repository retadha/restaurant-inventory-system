from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ResepForm
from .models import Resep
from django.contrib.auth.decorators import login_required
from propensi.utils import is_restoran

@login_required(login_url='/login/')
def create(request):
    if (is_restoran(request) == False):
        return render(request, 'error/403.html')
    if request.method == "POST":
        add = ResepForm(request.POST)
        if add.is_valid():
            namaResep = add.cleaned_data.get('nama')
            add.save()
            messages.success(request, f'Resep {namaResep} berhasil dibuat.')
            return redirect("resep:list")
        else:
            messages.error(
                request, f'Input gagal. Resep {add.instance.nama} sudah terdaftar.')
            return redirect("resep:list")
    add = ResepForm()
    return render(request, 'create.html', {'form':add})

@login_required(login_url='/login/')
def list(request):
    if (is_restoran(request) == False):
        return render(request, 'error/403.html')
    daftar_resep = Resep.objects.all()
    context = {
        "daftar_resep" : daftar_resep
    }
    return render(request, 'list.html', context)

@login_required(login_url='/login/')
def view(request, id_resep):
    if (is_restoran(request) == False):
        return render(request, 'error/403.html')
    resep = Resep.objects.get(pk=id_resep)
    context = {
        "id_resep" : resep.id_resep,
        "nama" : resep.nama,
        "bahan" : resep.bahan,
        "cara_memasak" : resep.cara_memasak
    }
    return render(request, 'view.html', context)

@login_required(login_url='/login/')
def update(request, id_resep):
    if (is_restoran(request) == False):
        return render(request, 'error/403.html')
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
        return HttpResponseRedirect('/resep/')

    context = {
        'id_resep' : resep.id_resep,
        'nama' : resep.nama,
        'bahan' : resep.bahan,
        'cara_memasak' : resep.cara_memasak

    }
    return render(request, "update.html", context)

@login_required(login_url='/login/')
def delete(request, id_resep):
    if (is_restoran(request) == False):
        return render(request, 'error/403.html')
    try:
        resep = Resep.objects.get(pk=id_resep)
        resep.delete()
        return HttpResponseRedirect('/resep/')
    except Resep.DoesNotExist:
        raise Http404("Objek tidak ditemukan")
