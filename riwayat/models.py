from django.db import models

# Create your models here.

class Riwayat(models.Model):
    id_riwayat = models.AutoField(primary_key=True)
    product = models.CharField(max_length=200, null=False, blank=False)
    total = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    notes = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.product

