# Generated by Django 5.1.3 on 2024-11-25 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_sucursal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen_producto',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
    ]