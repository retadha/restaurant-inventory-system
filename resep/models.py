from django.db import models

class Resep(models.Model):
    id_resep = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50, null=False, blank=False)
    bahan = models.TextField(null=False, blank=False)
    cara_memasak = models.TextField(null=False, blank=False)
    gambar = models.ImageField(upload_to='resep/', help_text='Please use .jpg format')
    
    def __str__(self) -> str:
        return self.nama
