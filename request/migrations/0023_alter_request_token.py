# Generated by Django 3.2 on 2023-05-02 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0022_alter_request_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='token',
            field=models.CharField(default='JT4F7', max_length=5),
        ),
    ]
