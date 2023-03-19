from django.db import models

class Gedung(models.Model):
    id_gedung = models.AutoField(primary_key=True, unique=True)
    nama = models.CharField(max_length=100)
    alamat = models.CharField(max_length=100)
    status = models.CharField(max_length=5)

    def __str__(self):
        return self.nama