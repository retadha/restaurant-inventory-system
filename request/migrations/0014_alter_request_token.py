# Generated by Django 3.2 on 2023-05-01 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0013_alter_request_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='token',
            field=models.CharField(default='R0S6U', max_length=5),
        ),
    ]
