from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserChangeForm
from employee.forms import E164_REGEX


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()
    nohp = forms.CharField(validators=[
        RegexValidator(E164_REGEX, "Please enter a valid phone number.")
    ])
    
    class Meta:
        model = User
        fields = ('email', 'nohp')
        
    def save(self):
        user = super(UserUpdateForm, self).save()
        user.save()
         
        

