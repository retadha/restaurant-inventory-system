from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from employee.forms import E164_REGEX
from gedung.models import Gedung


class UserUpdateForm(forms.ModelForm):
    nama = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=[('0', 'Manager'), ('1', 'Staff')])
    email = forms.EmailField()
    nohp = forms.CharField(validators=[
        RegexValidator(E164_REGEX, "Please enter a valid phone number.")
    ])
    id_gedung = forms.ModelChoiceField(queryset=Gedung.objects.all())

    class Meta:
        model = User
        fields = ('username', 'nama', 'role', 'email', 'nohp', 'id_gedung')