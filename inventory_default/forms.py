from django import forms
from .models import InventoryDefault

class InventoryDefaultForm(forms.ModelForm):
    class Meta:
        model = InventoryDefault
        fields = ['id_inventory_default','nama', 'satuan', 'harga']