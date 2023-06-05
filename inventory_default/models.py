from django.db import models

from gedung.models import Gedung

class InventoryDefault(models.Model):
    id_inventory_default = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50, null=False, blank=False, unique=True, error_messages={'unique':"This name has already been registered."})
    satuan = models.CharField(max_length=20, null=False, blank=False)
    harga = models.DecimalField(max_digits=20, decimal_places=0, null=False, blank=False)
    
    def __str__(self) -> str:
        return self.nama
    
    def save(self, *args, **kwargs):
        from inventory.models import Inventory
        super().save(*args, **kwargs)
        ged = list(Gedung.objects.values_list('id_gedung', flat=True))
        for a in ged:
            Inventory.objects.update_or_create(
                default_id = self.id_inventory_default,
                stok = 0,
                threshold = 0,
                default_request_qty = 0,
                id_gedung = Gedung.objects.get(id_gedung = a)
            )