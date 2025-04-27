from django.db import models
from django.core.exceptions import ValidationError
from .inventario import Producto
from .base import Usuario

# Opciones para los tipos de movimientos que se pueden realizar en el inventario
TIPO_MOVIMIENTO_CHOICES = [
    ('Entrada', 'Entrada'),
    ('Salida', 'Salida'),
    ('Ajuste', 'Ajuste'), 
]

# Modelo Kardex: Registra todos los movimientos de inventario y mantiene el control de costos
class Kardex(models.Model):
    producto_kardex = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_kardex = models.DateTimeField(auto_now_add=True)
    tipo_kardex = models.CharField(max_length=10,choices=TIPO_MOVIMIENTO_CHOICES,null=False)
    cantidad_kardex = models.IntegerField(null=False)
    costo_unitario_kardex = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    costo_total_kardex = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    saldo_cantidad_kardex = models.IntegerField(null=False)
    saldo_costo_kardex = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    referencia_kardex = models.TextField(blank=True, null=True)

    # Método de validación para evitar salidas de inventario cuando no hay suficiente stock
    def clean(self):
        super().clean()
        if self.tipo_kardex == 'Salida' and self.saldo_cantidad_kardex < self.cantidad_kardex:
            raise ValidationError(
                f"No puedes registrar una salida de {self.cantidad_kardex} unidades, "
                f"ya que el saldo actual es de {self.saldo_cantidad_kardex} unidades."
            )

    # Configuración de índices para optimizar las búsquedas frecuentes
    class Meta:
        indexes = [
            models.Index(fields=['fecha_kardex'], name='idx_fecha_kardex'),
            models.Index(fields=['producto_kardex'], name='idx_producto_kardex'),
            #Posible uso a futuro para realizar busquedas por tipo de movimiento
            models.Index(fields=['tipo_kardex'], name='idx_tipo_kardex'),
        ]

    def __str__(self):
        return f"{self.id} | {self.producto_kardex.nombre_producto} | {self.tipo_kardex} | {self.cantidad_kardex} unidades"

# Modelo MovimientoInventario: Registra los movimientos de inventario incluyendo información del usuario que los realiza
class MovimientoInventario(models.Model):
    producto_movimientoInventario = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario_movimientoInventario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    tipo_movimientoInventario = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad_movimientoInventario = models.IntegerField(null=False)
    fecha_movimientoInventario = models.DateTimeField(auto_now_add=True)
    motivo_movimientoInventario = models.TextField(blank=True, null=True)
    kardex_movimiento = models.OneToOneField(Kardex, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.producto_movimientoInventario.nombre_producto} | {self.tipo_movimientoInventario} | {self.cantidad_movimientoInventario} unidades"
