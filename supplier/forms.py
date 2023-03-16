from django import forms
from .models import Supplier

class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['nama','alamat','pic','nohp']