from django import forms

from gedung.models import Gedung
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['id_inventory','nama', 'stok', 'threshold', 'default_request_qty', 'harga', 'satuan']