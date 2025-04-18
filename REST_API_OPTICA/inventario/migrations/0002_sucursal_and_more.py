# Generated by Django 5.1.3 on 2024-11-25 02:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sucursal', models.TextField()),
                ('direccion_sucursal', models.TextField()),
                ('telefono_sucursal', models.TextField(blank=True, null=True)),
                ('activo_sucursal', models.BooleanField(default=True)),
                ('fecha_creacion_sucursal', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='productoproveedor',
            old_name='porducto_productoProveedor',
            new_name='producto_productoProveedor',
        ),
        migrations.AddField(
            model_name='producto',
            name='sucursal_producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.sucursal'),
        ),
        migrations.AddField(
            model_name='venta',
            name='sucursal_venta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.sucursal'),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.TextField()),
                ('apellido_usuario', models.TextField()),
                ('email_usuario', models.EmailField(max_length=254, unique=True)),
                ('telefono_usuario', models.TextField(blank=True, null=True)),
                ('rol_usuario', models.CharField(choices=[('Administrador', 'Administrador'), ('Gerente', 'Gerente'), ('Usuario', 'Usuario')], default='Usuario', max_length=20)),
                ('fecha_creacion_usuario', models.DateTimeField(auto_now_add=True)),
                ('activo_usuario', models.BooleanField(default=True)),
                ('sucursal_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.sucursal')),
            ],
        ),
        migrations.AddField(
            model_name='movimientoinventario',
            name='usuario_movimientoInventario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.usuario'),
        ),
        migrations.AddField(
            model_name='venta',
            name='usuario_venta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.usuario'),
        ),
    ]
