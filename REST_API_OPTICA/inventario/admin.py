from django.contrib import admin
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, Usuario, Sucursal, Kardex, FichaMedica, Abono, Paciente
from django.contrib.auth.models import User

# Cambiar el título y encabezados del panel

# Registra los modelos
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(ProductoProveedor)
admin.site.register(Venta)
admin.site.register(Cliente)
admin.site.register(ArticuloVenta)
admin.site.register(MovimientoInventario)
admin.site.register(Lote)
admin.site.register(Usuario)
admin.site.register(Sucursal)
admin.site.register(Kardex)
admin.site.register(FichaMedica)
admin.site.register(Abono)
admin.site.register(Paciente)
