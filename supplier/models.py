from django.db import models

# Create your models here.
class Supplier(models.Model):
    id_supplier = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100, null=False, blank=False)
    alamat = models.TextField(null=False, blank=False)
    pic = models.CharField(max_length=100, null=False, blank=False)
    nohp = models.CharField(max_length=25, null=False, blank=False)

    def __str__(self):
        return self.nama
