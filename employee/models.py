from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from gedung.models import Gedung

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[('0', 'MANAGER'), ('1', 'STAFF'), ('2', 'ADMIN')])
    email = models.CharField(max_length=100)
    
    phone_regex = RegexValidator(regex=r"^(\+[1-9])?\d{1,14}$", message="Masukkan nomor telepon dengan benar")

    nohp = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    id_gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username