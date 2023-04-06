from django import forms

from gedung.models import Gedung
from .models import Inventori

class InventoriForm(forms.ModelForm):
    class Meta:
        model = Inventori
        fields = ['id_inventory','nama', 'stok', 'threshold', 'default_request_qty', 'harga', 'satuan']