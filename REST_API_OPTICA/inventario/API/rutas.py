from rest_framework.routers import DefaultRouter
from django.urls import path
from inventario.API.vistas import (
    categoriaViewSet, productoViewSet, proveedorViewSet, productoProveedorViewSet,
    clienteViewSet, ventaViewSet, articuloVentaViewSet, movimientoInventarioViewSet,
    loteViewSet, UserViewSet, usuarioViewSet, sucursalViewSet, ProductoFiltradoPorCategoria, kardexViewSet,
    KardexPorProductoAPIView, obtener_id_usuario
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
]

urlpatterns += router.urls
