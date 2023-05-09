from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def pembelian(request):
    context = {
        'title': "Transaksi Pembelian",
        # 'profile': profile
    }
    template = 'laporan/pembelian.html'  
    return render(request, template, context)

