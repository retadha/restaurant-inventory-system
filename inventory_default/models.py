from django.db import models

class InventoryDefault(models.Model):
    id_inventory_default = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50, null=False, blank=False, unique=True, error_messages={'unique':"This name has already been registered."})
    satuan = models.CharField(max_length=20, null=False, blank=False)
    harga = models.DecimalField(max_digits=20, decimal_places=3, null=False, blank=False)
    
    def __str__(self) -> str:
        return self.nama
    