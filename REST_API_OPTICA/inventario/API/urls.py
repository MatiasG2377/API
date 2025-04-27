
from django.db import router
from rest_framework.routers import DefaultRouter
from django.urls import path
from inventario.API.views.abonos import (
    AbonoViewSet,
    buscar_abonos_dinamico,
    historial_abonos_por_cliente
)
from inventario.API.views.clientes import (
    ClienteViewSet,
    buscar_clientes_dinamico,
    cliente_por_ci_exacto
)
from inventario.API.views.fichas import (
    FichaMedicaViewSet,
    buscar_fichas_dinamico,
    fichas_por_paciente
)
from inventario.API.views.productos import (
    ProductoViewSet,
    buscar_productos_dinamico,
    producto_por_codigo
)
from inventario.API.views.dashboard import (
    dashboard_ventas_por_mes,
    dashboard_top_productos,
    dashboard_ingresos_por_sucursal,
    dashboard_movimientos_por_mes,
    dashboard_evolucion_stock_producto,
    dashboard_productos_bajo_stock
)
from inventario.API.views.ventas import (
    VentaViewSet,
    ArticuloVentaViewSet,
    buscar_ventas_por_cliente,
    ventas_agrupadas_por_mes
)
from inventario.API.views.kardex import (
    KardexViewSet,
    historial_kardex_por_producto,
    evolucion_stock_producto,
)
from inventario.API.views.sucursal import (
    SucursalViewSet,
    buscar_sucursales_dinamico
)
from inventario.API.views.usuarios import (
    UsuarioViewSet,
    buscar_usuarios_dinamico,
    obtener_usuario_por_username
)
from inventario.API.views.movimiento_inventario import (
    MovimientoInventarioViewSet,
    buscar_movimientos_dinamico,
    movimientos_agrupados_por_mes
)
from inventario.API.views.proveedor import (
    ProveedorViewSet,
    buscar_proveedores_dinamico
)
from inventario.API.views.categoria import (
    CategoriaViewSet,
    buscar_categorias_dinamico
)
from inventario.API.views.paciente import (
    PacienteViewSet,
    buscar_pacientes_dinamico,
    obtener_paciente_por_ci
)
router = DefaultRouter()
router.register(r'abonos', AbonoViewSet, basename='abono')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'fichas-medicas', FichaMedicaViewSet, basename='ficha-medica')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'ventas', VentaViewSet, basename='ventas')
router.register(r'articulos-venta', ArticuloVentaViewSet, basename='articulos-venta')
router.register(r'kardex', KardexViewSet, basename='kardex')
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'movimientos-inventario', MovimientoInventarioViewSet, basename='movimiento-inventario')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'pacientes', PacienteViewSet, basename='paciente')

urlpatterns = [
    path('abonos/buscar/', buscar_abonos_dinamico, name='buscar-abonos-dinamico'),
    path('abonos/historial/', historial_abonos_por_cliente, name='historial-abonos-cliente'),
    path('clientes/buscar/', buscar_clientes_dinamico, name='buscar-clientes-dinamico'),
    path('clientes/ci/', cliente_por_ci_exacto, name='cliente-por-ci'),
    path('fichas/buscar/', buscar_fichas_dinamico, name='buscar-fichas-dinamico'),
    path('fichas/paciente/', fichas_por_paciente, name='fichas-por-paciente'),
    path('productos/buscar/', buscar_productos_dinamico, name='buscar-productos-dinamico'),
    path('productos/codigo/', producto_por_codigo, name='producto-por-codigo'),
    path('dashboard/ventas-por-mes/', dashboard_ventas_por_mes),
    path('dashboard/top-productos/', dashboard_top_productos),
    path('dashboard/ingresos-sucursal/', dashboard_ingresos_por_sucursal),
    path('dashboard/movimientos-inventario/', dashboard_movimientos_por_mes),
    path('dashboard/evolucion-stock/<int:producto_id>/', dashboard_evolucion_stock_producto),
    path('dashboard/productos-bajo-stock/', dashboard_productos_bajo_stock),
    path('ventas/buscar/', buscar_ventas_por_cliente, name='buscar-ventas-por-cliente'),
    path('ventas/reporte-mensual/', ventas_agrupadas_por_mes, name='ventas-agrupadas-por-mes'),
    path('kardex/historial/<int:producto_id>/', historial_kardex_por_producto),
    path('kardex/evolucion/<int:producto_id>/', evolucion_stock_producto),
    path('sucursales/buscar/', buscar_sucursales_dinamico),
    path('usuarios/buscar/', buscar_usuarios_dinamico),
    path('usuarios/obtener-id/', obtener_usuario_por_username),    
    path('movimientos-inventario/buscar/', buscar_movimientos_dinamico),
    path('dashboard/movimientos-por-mes/', movimientos_agrupados_por_mes),
    path('proveedores/buscar/', buscar_proveedores_dinamico),
    path('categorias/buscar/', buscar_categorias_dinamico),
    path('pacientes/buscar/', buscar_pacientes_dinamico),
    path('pacientes/ci/<str:ci>/', obtener_paciente_por_ci),
]
urlpatterns += router.urls