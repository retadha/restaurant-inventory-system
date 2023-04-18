from django.db import models
from gedung.models import Gedung
from inventory_default.models import InventoryDefault

class Inventory(models.Model):
    stok = models.IntegerField(null=False, blank=False)
    threshold = models.IntegerField(null=False, blank=False)
    default_request_qty = models.IntegerField(null=False, blank=False)

    id_gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE)
    default = models.ForeignKey(InventoryDefault, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.default} - {self.id_gedung.nama}"
    