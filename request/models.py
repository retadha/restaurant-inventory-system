from django.db import models
from employee.models import Employee
from gedung.models import Gedung
from supplier.models import Supplier
from inventory_default.models import InventoryDefault


class Request(models.Model):
    id_request = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, default="0", choices=[('0', 'WAITING FOR APPROVAL'), ('1', 'SUBMITTING'), ('2', 'PROCESSING'), ('3', 'COMPLETED')])
    approved = models.DateTimeField(null=True, blank=True)
    received = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=5, default='')

    pic = models.ForeignKey(Employee, on_delete=models.CASCADE)
    id_gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE)
    id_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def get_lines(self):
        return Inventory_Line.objects.filter(id_request=self.id_request)

    @property
    def total_price(self):
        total = 0
        for item in self.get_lines:
            total += item.qty * item.harga
        return total

    @property
    def status_gedung(self):
        return self.id_gedung.status

    def __str__(self):
        return f"{self.id_gedung} - {self.token}"

class Inventory_Line(models.Model):
    id_line = models.AutoField(primary_key=True)
    qty = models.IntegerField()
    harga = models.DecimalField(max_digits=20, decimal_places=0, null=False, blank=False)

    id_inventory_default = models.ForeignKey(InventoryDefault, on_delete=models.CASCADE)
    id_request = models.ForeignKey(Request, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_inventory_default} - {self.id_request}"
