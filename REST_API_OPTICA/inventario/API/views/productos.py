# Importaciones necesarias de Django Rest Framework
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Importaciones de modelos y serializadores locales
from inventario.models import Producto
from inventario.API.serializers import ProductoSerializer


# Clase para manejar la paginación de productos
class ProductoPagination(PageNumberPagination):
    # Tamaño de página por defecto
    page_size = 20
    # Parámetro para modificar el tamaño de página en la URL
    page_size_query_param = 'page_size'
    # Límite máximo de elementos por página
    max_page_size = 100


# ViewSet principal para el modelo Producto
class ProductoViewSet(viewsets.ModelViewSet):
    # Permite acceso sin autenticación
    permission_classes = [AllowAny]
    # Consulta que obtiene todos los productos con sus relaciones, ordenados por nombre
    queryset = Producto.objects.select_related('categoria_producto', 'proveedor_producto').order_by('nombre_producto')
    # Especifica el serializador a utilizar
    serializer_class = ProductoSerializer
    # Clase de paginación personalizada
    pagination_class = ProductoPagination


# Vista para búsqueda dinámica de productos
@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_productos_dinamico(request):
    """
    Buscador rápido por nombre o código del producto. Máx. 10 resultados.
    """
    # Obtiene y limpia el parámetro de búsqueda
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    # Realiza la búsqueda por nombre o código del producto
    productos = Producto.objects.filter(
        Q(nombre_producto__icontains=query) | Q(codigo_producto__icontains=query)
    ).order_by('nombre_producto')[:10]

    # Serializa y devuelve los resultados
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)


# Vista para buscar un producto por su código exacto
@api_view(['GET'])
@permission_classes([AllowAny])
def producto_por_codigo(request):
    """
    Devuelve un producto exacto por código. Útil para autocompletar formularios.
    """
    # Obtiene y limpia el código del producto
    codigo = request.query_params.get('codigo', '').strip()
    if not codigo:
        return Response({"detail": "Se requiere el parámetro 'codigo'"}, status=400)

    try:
        # Intenta obtener el producto por su código
        producto = Producto.objects.get(codigo_producto=codigo)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    except Producto.DoesNotExist:
        # Devuelve error 404 si no encuentra el producto
        return Response({"detail": "Producto no encontrado"}, status=404)
