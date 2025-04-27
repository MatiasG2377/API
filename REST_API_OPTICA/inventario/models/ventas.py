from django.db import models
from django.core.exceptions import ValidationError

# Importa los modelos relacionados
from .clientes import Cliente
from .base import Usuario, Sucursal

# Opciones de métodos de pago para ventas y abonos
# Define los tipos de pago válidos: Efectivo, Transferencia, Tarjeta y Crédito empresarial
METODO_PAGO_CHOICES = [
    ('Efectivo', 'Efectivo'),
    ('Transferencia', 'Transferencia'),
    ('Tarjeta', 'Tarjeta'),
    ('Crédito empresarial', 'Crédito empresarial'),
]

# Modelo de Venta - Representa una transacción de venta
# Contiene relaciones con cliente, usuario (vendedor), sucursal
# Incluye monto total, método de pago y fecha de venta
# Indexado por fecha y cliente para consultas más rápidas
class Venta(models.Model):
    cliente_venta = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    usuario_venta = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    sucursal_venta = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    metodo_venta = models.CharField(max_length=255, blank=True, null=True, choices=METODO_PAGO_CHOICES, default='Efectivo')

    class Meta:
        indexes = [
            models.Index(fields=['fecha_venta'], name='idx_fecha_venta'),
            models.Index(fields=['cliente_venta'], name='idx_cliente_venta'),
        ]

    def __str__(self):
        cliente = self.cliente_venta.nombre_cliente if self.cliente_venta else "—"
        usuario = f"{self.usuario_venta.nombre_usuario} {self.usuario_venta.apellido_usuario}" if self.usuario_venta else "—"
        total = self.total_venta or 0
        return f"#{self.id} | {cliente} | {usuario} | ${total:.2f}"

# Modelo de Abono - Representa pagos realizados para las ventas
# Rastrea monto de pago, fecha, método y enlaces a venta y cliente
# Indexado por fecha y cliente para consultas eficientes
class Abono(models.Model):
    venta = models.ForeignKey(Venta, null=True, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=100, choices=METODO_PAGO_CHOICES, default='Efectivo')

    class Meta:
        indexes = [
            models.Index(fields=['fecha'], name='idx_fecha_abono'),
            models.Index(fields=['cliente'], name='idx_cliente_abono'),
        ]

    def __str__(self):
        cliente = self.cliente.nombre_cliente if self.cliente else "—"
        return f"#{self.id} | {cliente} | ${self.monto:.2f}"

# Modelo de Artículo de Venta - Representa artículos individuales en una venta
# Vincula productos con ventas incluyendo cantidad y precio
# Incluye validación de stock para evitar sobreventa
# Indexado por venta y producto para mejor rendimiento
class ArticuloVenta(models.Model):
    venta_articuloVenta = models.ForeignKey(Venta, on_delete=models.CASCADE,)
    producto_articuloVenta = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE)
    cantidad_articuloVenta = models.IntegerField(null=False)
    pvp_articuloVenta = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def clean(self):
        super().clean()
        if self.cantidad_articuloVenta > self.producto_articuloVenta.cantidad_producto:
            raise ValidationError(
                f"La cantidad ({self.cantidad_articuloVenta}) no puede ser mayor que el stock disponible "
                f"({self.producto_articuloVenta.cantidad_producto}) del producto '{self.producto_articuloVenta.nombre_producto}'."
            )

    class Meta:
        indexes = [
            models.Index(fields=['venta_articuloVenta'], name='idx_venta_articuloVenta'),
            models.Index(fields=['producto_articuloVenta'], name='idx_producto_articuloVenta'),
        ]

    def __str__(self):
        return f"{self.id} | {self.producto_articuloVenta.nombre_producto} | {self.cantidad_articuloVenta}"