# Generated by Django 3.2 on 2023-03-18 19:02

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
