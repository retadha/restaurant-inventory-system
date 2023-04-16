from django.db import models
from employee.models import Employee
from gedung.models import Gedung
from supplier.models import Supplier
from inventory_default.models import InventoryDefault
# Create your models here.
class Request(models.Model):
    id_request = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, default="0", choices=[('0', 'WAITING FOR APPROVAL'), ('1', 'SUBMITTING'), ('2', 'PROCESSING'), ('3', 'COMPLETED')])
    created = models.DateTimeField(auto_now_add=True)
    received = models.DateTimeField(null=True, blank=True)

    pic = models.ForeignKey(Employee, on_delete=models.CASCADE)
    id_gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE)
    id_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    @property
    def get_lines(self):
        return Inventory_Line.objects.filter(id_request=self.id_request)

    @property
    def total_price(self):
        total = 0
        for item in self.get_lines:
            total += item.qty * item.harga
        return total

class Inventory_Line(models.Model):
    id_line = models.AutoField(primary_key=True)
    qty = models.IntegerField()
    harga = models.DecimalField(max_digits=20, decimal_places=3, null=False, blank=False)

    id_inventory_default = models.ForeignKey(InventoryDefault, on_delete=models.CASCADE)
    id_request = models.ForeignKey(Request, on_delete=models.CASCADE)
