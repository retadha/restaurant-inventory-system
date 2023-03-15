from django import forms
from .models import Resep

class AddResepForm(forms.ModelForm):
    class Meta:
        model = Resep
        fields = ['id_resep','nama', 'bahan', 'cara_memasak', 'gambar']
        