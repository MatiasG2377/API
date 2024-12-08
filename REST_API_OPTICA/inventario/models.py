from django.db import models
from django.core.exceptions import ValidationError

# Opciones para los estados de los productos
ESTADO_PRODUCTO_CHOICES = [
    ('Disponible', 'Disponible'),
    ('Reservado', 'Reservado'),
    ('Agotado', 'Agotado'),
]

# Opciones para los estados de las ventas
ESTADO_VENTA_CHOICES = [
    ('P', 'Pendiente'),
    ('C', 'Cancelado'),
    ('F', 'Finalizado'),
]

# Roles de los usuarios
ROLES_USUARIO_CHOICES = [
    ('Administrador', 'Administrador'),
    ('Gerente', 'Gerente'),
    ('Usuario', 'Usuario'),
]

# Tabla de Sucursales
class Sucursal(models.Model):
    nombre_sucursal = models.TextField(null=False)
    direccion_sucursal = models.TextField(null=False)
    telefono_sucursal = models.TextField(blank=True, null=True)
    activo_sucursal = models.BooleanField(default=True)
    fecha_creacion_sucursal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_sucursal


# Tabla de Usuarios
class Usuario(models.Model):
    nombre_usuario = models.TextField(null=False)
    apellido_usuario = models.TextField(null=False)
    email_usuario = models.EmailField(unique=True, null=False)
    telefono_usuario = models.TextField(blank=True, null=True)
    rol_usuario = models.CharField(max_length=20, choices=ROLES_USUARIO_CHOICES, default='Usuario')
    sucursal_usuario = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion_usuario = models.DateTimeField(auto_now_add=True)
    activo_usuario = models.BooleanField(default=True)
    username_usuario = models.CharField(max_length=150, unique=True, null=True, blank=True)  # Nuevo campo

    class Meta:
        indexes = [
            models.Index(fields=['email_usuario'], name='idx_email_usuario'),
        ]
    def __str__(self):
        return f"{self.nombre_usuario} {self.apellido_usuario} - {self.rol_usuario}"


# Categoría de productos
class Categoria(models.Model):
    nombre_categoria = models.TextField(null=False)
    descripcion_categoria = models.TextField(blank=True, null=True)
    activo_categoria = models.BooleanField(default=True)
    relevancia_categoria = models.IntegerField(default=0)
    fecha_creacion_categoria = models.DateTimeField(auto_now_add=True)
    actualizacion_categoria = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_categoria


# Proveedores
class Proveedor(models.Model):
    nombre_proveedor = models.TextField(null=False)
    informacion_proveedor = models.TextField(blank=True, null=True)
    correo_proveedor = models.EmailField(unique=True, blank=True, null=True)
    telefono_proveedor = models.TextField(blank=True, null=True)
    direccion_proveedor = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_proveedor


# Productos
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


# Relación entre Productos y Proveedores
class ProductoProveedor(models.Model):
    producto_productoProveedor = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor_productoProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    costo_productoProveedor = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_entrega_productoProveedor = models.IntegerField(help_text="Días para entrega", blank=True, null=True)

    def __str__(self):
        return f"{self.proveedor_productoProveedor.nombre_proveedor} - {self.producto_productoProveedor.nombre_producto}"


# Ventas
class Venta(models.Model):
    cliente_venta = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, blank=True)
    usuario_venta = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    sucursal_venta = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado_venta = models.CharField(max_length=1, choices=ESTADO_VENTA_CHOICES, default='P')
    metodo_venta = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['fecha_venta'], name='idx_fecha_venta'),
        ]
    def __str__(self):
        return f"Venta #{self.id} - {self.sucursal_venta.nombre_sucursal}"


# Movimientos de inventario
class MovimientoInventario(models.Model):
    producto_movimientoInventario = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario_movimientoInventario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    tipo_movimientoInventario = models.CharField(max_length=10, choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')])
    cantidad_movimientoInventario = models.IntegerField(null=False)
    fecha_movimientoInventario = models.DateTimeField(auto_now_add=True)
    motivo_movimientoInventario = models.TextField(blank=True, null=True)
    kardex_movimiento = models.OneToOneField('Kardex', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_movimientoInventario} - {self.producto_movimientoInventario.nombre_producto} ({self.cantidad_movimientoInventario})"


# Clientes
class Cliente(models.Model):
    ci_cliente = models.TextField(null=False)
    nombre_cliente = models.TextField(null=False)
    informacion_cliente = models.TextField(blank=True, null=True)
    correo_cliente = models.EmailField(unique=True, blank=True, null=True)
    telefono_cliente = models.TextField(blank=True, null=True)
    direccion_cliente = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_cliente


# Artículos vendidos en una venta
class ArticuloVenta(models.Model):
    venta_articuloVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto_articuloVenta = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_articuloVenta = models.IntegerField(null=False)
    pvp_articuloVenta = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    descuento_articuloVenta = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    def clean(self):
        super().clean()
        if self.cantidad_articuloVenta > self.producto_articuloVenta.cantidad_producto:
            raise ValidationError(
                f"La cantidad ({self.cantidad_articuloVenta}) no puede ser mayor que el stock disponible "
                f"({self.producto_articuloVenta.cantidad_producto}) del producto '{self.producto_articuloVenta.nombre_producto}'."
            )
    def __str__(self):
        return f"Artículo {self.producto_articuloVenta.nombre_producto} en Venta #{self.venta_articuloVenta.id}"


# Lotes de productos
class Lote(models.Model):
    producto_lote = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_lote = models.IntegerField()
    fecha_ingreso_lote = models.DateTimeField(auto_now_add=True)
    fecha_caducidad_lote = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Lote de {self.producto_lote.nombre_producto} ({self.cantidad_lote} unidades)"


# Kardex
class Kardex(models.Model):
    producto_kardex = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_kardex = models.DateTimeField(auto_now_add=True)
    tipo_kardex = models.CharField(
        max_length=10,
        choices=[('Entrada', 'Entrada'), ('Salida', 'Salida'), ('Ajuste', 'Ajuste')],
        null=False
    )
    cantidad_kardex = models.IntegerField(null=False)
    costo_unitario_kardex = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    costo_total_kardex = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    saldo_cantidad_kardex = models.IntegerField(null=False)
    saldo_costo_kardex = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    referencia_kardex = models.TextField(blank=True, null=True)
    lote_kardex = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True)
    def clean(self):
        super().clean()
        # Si el movimiento es una salida, verifica que no se genere un saldo negativo
        if self.tipo_kardex == 'Salida' and self.saldo_cantidad_kardex < self.cantidad_kardex:
            raise ValidationError(
                f"No puedes registrar una salida de {self.cantidad_kardex} unidades, "
                f"ya que el saldo actual es de {self.saldo_cantidad_kardex} unidades."
            )
    class Meta:
        indexes = [
            models.Index(fields=['fecha_kardex'], name='idx_fecha_kardex'),
        ]
    def __str__(self):
        return f"Kardex de {self.producto_kardex.nombre_producto} - {self.tipo_kardex} ({self.fecha_kardex})"
