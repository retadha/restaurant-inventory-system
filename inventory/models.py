from django.db import models
from gedung.models import Gedung
from inventory_default.models import InventoryDefault
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


class Inventory(models.Model):
    id_inventory = models.AutoField(primary_key=True)
    stok = models.IntegerField(null=False, blank=False)
    threshold = models.IntegerField(null=False, blank=False)
    default_request_qty = models.IntegerField(null=False, blank=False)

    id_gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE)
    default = models.ForeignKey(InventoryDefault, on_delete=models.CASCADE)

    def __str__(self):
        return (self.default.nama + " - " + self.id_gedung.nama)
    
