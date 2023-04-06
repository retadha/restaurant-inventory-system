# Generated by Django 4.2 on 2023-04-06 08:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gedung', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('0', 'MANAGER'), ('1', 'STAFF'), ('2', 'ADMIN')], max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('nohp', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Masukkan nomor telepon dengan benar', regex='^(\\+[1-9])?\\d{1,14}$')])),
                ('id_gedung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gedung.gedung')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
