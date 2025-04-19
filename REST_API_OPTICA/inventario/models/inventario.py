from django.db import models
from django.core.exceptions import ValidationError
from .base import Sucursal
from .clientes import Cliente

ESTADO_PRODUCTO_CHOICES = [
    ('Disponible', 'Disponible'),
    ('Reservado', 'Reservado'),
    ('Agotado', 'Agotado'),
]

class Categoria(models.Model):
    nombre_categoria = models.TextField(null=False)
    descripcion_categoria = models.TextField(blank=True, null=True)
    activo_categoria = models.BooleanField(default=True)
    relevancia_categoria = models.IntegerField(default=0)
    fecha_creacion_categoria = models.DateTimeField(auto_now_add=True)
    actualizacion_categoria = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_categoria

class Proveedor(models.Model):
    nombre_proveedor = models.TextField(null=False)
    informacion_proveedor = models.TextField(blank=True, null=True)
    correo_proveedor = models.EmailField(unique=True, blank=True, null=True)
    telefono_proveedor = models.TextField(blank=True, null=True)
    direccion_proveedor = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_proveedor

class Producto(models.Model):
    nombre_producto = models.TextField(null=False)
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    pvp_producto = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    costo_producto = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_producto = models.IntegerField(null=False)
    minimo_producto = models.IntegerField(default=0)
    maximo_producto = models.IntegerField(default=100)
    sucursal_producto = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)
    fecha_ingreso_producto = models.DateTimeField(auto_now_add=True)
    estado_producto = models.CharField(max_length=20, choices=ESTADO_PRODUCTO_CHOICES, default='Disponible')
    descripcion_producto = models.TextField(blank=True, null=True)
    marca_producto = models.TextField(blank=True, null=True)
    proveedores_producto = models.ManyToManyField(Proveedor, through='ProductoProveedor')
    ultima_venta_producto = models.DateTimeField(blank=True, null=True)
    imagen_producto = models.URLField(max_length=500, blank=True, null=True)
    metodo_valoracion = models.CharField(
        max_length=10,
        choices=[('PEPS', 'PEPS'), ('UEPS', 'UEPS'), ('Promedio', 'Promedio')],
        default='Promedio'
    )

    class Meta:
        indexes = [
            models.Index(fields=['nombre_producto'], name='idx_nombre_producto'),
        ]
    def clean(self):
        if self.minimo_producto > self.maximo_producto:
            raise ValidationError("El stock mínimo no puede ser mayor que el stock máximo.")
        if self.cantidad_producto < 0:
            raise ValidationError("La cantidad en stock no puede ser negativa.")

    def __str__(self):
        return f"{self.nombre_producto} - {self.sucursal_producto.nombre_sucursal}"

class ProductoProveedor(models.Model):
    producto_productoProveedor = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor_productoProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    costo_productoProveedor = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_entrega_productoProveedor = models.IntegerField(help_text="Días para entrega", blank=True, null=True)

    def __str__(self):
        return f"{self.proveedor_productoProveedor.nombre_proveedor} - {self.producto_productoProveedor.nombre_producto}"

class Lote(models.Model):
    producto_lote = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_lote = models.IntegerField()
    fecha_ingreso_lote = models.DateTimeField(auto_now_add=True)
    fecha_caducidad_lote = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Lote de {self.producto_lote.nombre_producto} ({self.cantidad_lote} unidades)"
