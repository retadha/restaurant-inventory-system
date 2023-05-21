from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from request.models import Request

@login_required(login_url='/login/')
def pembelian(request):
    pembelian = Request.objects.filter(id_gedung__status__exact="0", status="3")
    context = {
        'requests': pembelian

    }

    return render(request, 'riwayat/pembelian.html', context)
