# Generated by Django 3.2 on 2023-04-16 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
        ('supplier', '0001_initial'),
        ('gedung', '0001_initial'),
        ('inventory_default', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id_request', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('0', 'WAITING FOR APPROVAL'), ('1', 'SUBMITTING'), ('2', 'PROCESSING'), ('3', 'COMPLETED')], max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('received', models.DateTimeField()),
                ('id_gedung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gedung.gedung')),
                ('id_supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier')),
                ('pic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory_Line',
            fields=[
                ('id_line', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField()),
                ('harga', models.DecimalField(decimal_places=3, max_digits=20)),
                ('id_inventory_default', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_default.inventorydefault')),
                ('id_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.request')),
            ],
        ),
    ]