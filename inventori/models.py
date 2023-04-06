from django.db import models
from django.contrib.auth.models import User
from gedung.models import Gedung

class Inventori(models.Model):
    id_inventory = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50, null=False, blank=False)
    stok = models.IntegerField(null=False, blank=False)
    threshold = models.IntegerField(null=False, blank=False)
    default_request_qty = models.IntegerField(null=False, blank=False)
    harga = models.DecimalField(max_digits=20, decimal_places=3, null=False, blank=False)
    satuan = models.CharField(max_length=20, null=False, blank=False)

    
    id_gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE)

    
    def __str__(self) -> str:
        return self.nama