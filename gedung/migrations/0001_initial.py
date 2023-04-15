# Generated by Django 4.2 on 2023-04-15 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gedung',
            fields=[
                ('id_gedung', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nama', models.CharField(max_length=100)),
                ('alamat', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('0', 'GUDANG PUSAT'), ('1', 'RESTORAN')], max_length=15)),
            ],
        ),
    ]
