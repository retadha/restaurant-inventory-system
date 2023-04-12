from django import forms

from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['id_inventory', 'id_inventory_default', 'stok', 'threshold', 'default_request_qty']