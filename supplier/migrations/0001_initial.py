# Generated by Django 4.2.1 on 2023-05-08 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id_supplier', models.AutoField(primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=100)),
                ('alamat', models.TextField()),
                ('pic', models.CharField(max_length=100)),
                ('nohp', models.CharField(max_length=25)),
            ],
        ),
    ]
