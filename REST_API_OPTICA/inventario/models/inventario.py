from django.db import models
from django.core.exceptions import ValidationError
from .base import Sucursal

# Modelo para gestionar categorías de productos
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100,null=False)
    descripcion_categoria = models.TextField(blank=True, null=True)
    fecha_creacion_categoria = models.DateTimeField(auto_now_add=True)
    actualizacion_categoria = models.DateTimeField(auto_now=True)
    # Índice para optimizar búsquedas por nombre
    class Meta:
        indexes = [
            models.Index(fields=['nombre_categoria'], name='idx_nombre_categoria'),
        ]
    def __str__(self):
        return f'{self.id} | {self.nombre_categoria}'

# Modelo para gestionar información de proveedores
class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=150, null=False)
    informacion_proveedor = models.TextField(blank=True, null=True)
    correo_proveedor = models.EmailField(unique=True, blank=True, null=True)
    telefono_proveedor = models.TextField(blank=True, null=True)
    direccion_proveedor = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} | {self.nombre_proveedor}"

# Modelo principal para gestión de productos
from django.db import models
from django.core.exceptions import ValidationError
from .base import Sucursal

class Producto(models.Model):
    nombre_producto = models.TextField(null=False)
    codigo_producto = models.CharField(max_length=20, unique=True, null=True, blank=True)
    proveedor_producto = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True)
    categoria_producto = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)
    pvp_producto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    costo_producto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cantidad_producto = models.IntegerField(null=True)
    minimo_producto = models.IntegerField(default=0, null=True)
    maximo_producto = models.IntegerField(default=100, null=True)
    sucursal_producto = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)
    fecha_ingreso_producto = models.DateTimeField(auto_now_add=True)
    descripcion_producto = models.TextField(blank=True, null=True)
    marca_producto = models.TextField(blank=True, null=True)
    imagen_producto = models.URLField(max_length=500, blank=True, null=True)
    controla_stock = models.BooleanField(default=True)

    @property
    def estado_producto(self):
        if not self.controla_stock:
            return '—'
        if self.cantidad_producto is None:
            return 'Desconocido'
        if self.cantidad_producto == 0:
            return 'Agotado'
        elif self.cantidad_producto <= self.minimo_producto:
            return 'Reservado'
        return 'Disponible'

    class Meta:
        indexes = [
            models.Index(fields=['nombre_producto'], name='idx_nombre_producto'),
        ]

    def clean(self):
        if self.minimo_producto > self.maximo_producto:
            raise ValidationError({
                'minimo_producto': "El stock mínimo no puede ser mayor que el stock máximo."
            })

        if self.controla_stock and self.cantidad_producto is not None and self.cantidad_producto < 0:
            raise ValidationError({
                'cantidad_producto': "La cantidad en stock no puede ser negativa para productos que controlan stock."
            })

    def __str__(self):
        return f"{self.id} | {self.nombre_producto}"

