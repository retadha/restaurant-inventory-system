# Generated by Django 4.2 on 2023-04-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resep',
            fields=[
                ('id_resep', models.AutoField(primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=50)),
                ('bahan', models.TextField()),
                ('cara_memasak', models.TextField()),
            ],
        ),
    ]
