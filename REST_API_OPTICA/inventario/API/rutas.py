from rest_framework.routers import DefaultRouter
from django.urls import path
from inventario.API.vistas import (
    categoriaViewSet, productoViewSet, proveedorViewSet, productoProveedorViewSet,
    clienteViewSet, ventaViewSet, articuloVentaViewSet, movimientoInventarioViewSet,
    loteViewSet, UserViewSet, usuarioViewSet, sucursalViewSet, ProductoFiltradoPorCategoria, kardexViewSet,
    KardexPorProductoAPIView, obtener_id_usuario, ProductosBajoStockAPIView, VentasPorSucursalAPIView, HistorialKardexAPIView,
    VentasPorMesAPIView, TopProductosVendidosAPIView, IngresosPorSucursalAPIView,MovimientosInventarioPorMesAPIView,
    EvolucionStockProductoAPIView, GenerateCustomChartView, ModelFieldsView, ListModelsView
)



router = DefaultRouter()
router.register('categoria', categoriaViewSet, basename='categoria')
router.register('producto', productoViewSet, basename='producto')
router.register('proveedor', proveedorViewSet, basename='proveedor')
router.register('productoproveedor', productoProveedorViewSet, basename='productoproveedor')
router.register('cliente', clienteViewSet, basename='cliente')
router.register('venta', ventaViewSet, basename='venta')
router.register('articuloventa', articuloVentaViewSet, basename='articuloventa')
router.register('movimiento', movimientoInventarioViewSet, basename='movimiento')
router.register('lotes', loteViewSet, basename='lote')
router.register('user', UserViewSet, basename='users')
router.register('usuario', usuarioViewSet, basename='usuarios')
router.register('sucursal', sucursalViewSet, basename='sucursales')
router.register(r'kardex', kardexViewSet, basename='kardex')
urlpatterns = [
    path('productos-filtrados/', ProductoFiltradoPorCategoria.as_view(), name='productos-filtrados'),
    path('kardex/<int:producto_id>/', KardexPorProductoAPIView.as_view(), name='kardex-por-producto'),
    path('usuario/obtener-id/', obtener_id_usuario, name='obtener_id_usuario'),
    path('productos/bajo_stock/', ProductosBajoStockAPIView.as_view(), name='productos_bajo_stock'),
    path('ventas/por_sucursal/', VentasPorSucursalAPIView.as_view(), name='ventas_por_sucursal'),
    path('kardex/historial/<int:producto_id>/', HistorialKardexAPIView.as_view(), name='historial_kardex'),
    path('ventas/por_mes/', VentasPorMesAPIView.as_view(), name='ventas_por_mes'),
    path('productos/top_vendidos/', TopProductosVendidosAPIView.as_view(), name='top_productos_vendidos'),
    path('ingresos/por_sucursal/', IngresosPorSucursalAPIView.as_view(), name='ingresos_por_sucursal'),
    path('movimientos/inventario_por_mes/', MovimientosInventarioPorMesAPIView.as_view(), name='movimientos_inventario_por_mes'),
    path('evolucion/stock/<int:producto_id>/', EvolucionStockProductoAPIView.as_view(), name='evolucion_stock_producto'),
    path('generate-chart/', GenerateCustomChartView.as_view(), name='generate-chart'),
    path('model-fields/<str:model_name>/', ModelFieldsView.as_view(), name='model-fields'),
    path('models/', ListModelsView.as_view(), name='list-models'),

]

urlpatterns += router.urls
