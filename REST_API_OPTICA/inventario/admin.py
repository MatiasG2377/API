from django.contrib import admin
from inventario.models import Categoria, Proveedor, Producto, Cliente, Venta, ArticuloVenta, MovimientoInventario, Usuario, Sucursal, Kardex, FichaMedica, Abono, Paciente

# Cambiar el título y encabezados del panel

# Registra los modelos
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Venta)
admin.site.register(Cliente)
admin.site.register(ArticuloVenta)
admin.site.register(MovimientoInventario)
admin.site.register(Usuario)
admin.site.register(Sucursal)
admin.site.register(Kardex)
admin.site.register(FichaMedica)
admin.site.register(Abono)
admin.site.register(Paciente)
