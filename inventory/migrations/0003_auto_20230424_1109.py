# Generated by Django 3.2 on 2023-04-24 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20230424_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='id_inventory',
        ),
        migrations.AddField(
            model_name='inventory',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]