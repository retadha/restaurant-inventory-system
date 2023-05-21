import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee
from django.core.validators import RegexValidator
from gedung.models import Gedung

E164_REGEX = re.compile(r"^(\+[1-9])?\d{1,14}$")

class EmployeeCreationForm(UserCreationForm):
    nama = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=[('0', 'Manager'), ('1', 'Staff')])
    email = forms.EmailField()
    nohp = forms.CharField(validators=[
        RegexValidator(E164_REGEX, "Please enter a valid phone number.")
    ])
    id_gedung = forms.ModelChoiceField(queryset=Gedung.objects.all())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nama', 'role', 'email', 'nohp', 'id_gedung')

    def save(self, commit=True):
        user = super(EmployeeCreationForm, self).save(commit=False)
        user.save()
        employee = Employee.objects.create(
            user=user, 
            nama=self.cleaned_data['nama'],
            role=self.cleaned_data['role'],
            email=self.cleaned_data['email'],
            nohp=self.cleaned_data['nohp'],
            id_gedung=self.cleaned_data['id_gedung'],
            )
        if commit:
            employee.save()
        return employee
