# Importaciones necesarias de Django Rest Framework para vistas, decoradores, permisos y paginación
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# Importaciones de modelos y serializadores locales
from inventario.models import Abono
from inventario.API.serializers import AbonoReadSerializer, AbonoWriteSerializer

# Clase para manejar la paginación de resultados
# Define un tamaño de página de 10 elementos, con un límite máximo de 100
class paginacion(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100

# ViewSet principal para el modelo Abono
# Permite operaciones CRUD completas y ordena los resultados por fecha descendente
class AbonoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Abono.objects.select_related('cliente', 'venta').order_by('-fecha')

    # Método para seleccionar el serializador apropiado según el tipo de petición
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AbonoWriteSerializer
        return AbonoReadSerializer


# Vista para búsqueda dinámica de abonos
# Implementa un autocompletado basado en el nombre del cliente
@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_abonos_dinamico(request):
    # Buscador dinámico (autocomplete) de abonos por nombre parcial del cliente.
    # Devuelve máx. 10 resultados para autocompletado.
    query = request.query_params.get('q', '').strip()

    if not query:
        return Response([], status=200)

    # Realiza una búsqueda case-insensitive en el nombre del cliente
    abonos = Abono.objects.filter(
        cliente__nombre_cliente__icontains=query
    ).select_related('cliente', 'venta')[:10]

    serializer = AbonoReadSerializer(abonos, many=True)
    return Response(serializer.data)


# Vista para obtener el historial completo de abonos de un cliente
# Incluye paginación de resultados
@api_view(['GET'])
@permission_classes([AllowAny])
def historial_abonos_por_cliente(request):
    # ?Devuelve el historial paginado de abonos filtrando por nombre parcial del cliente.
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response({"detail": "Se requiere el parámetro 'q'"}, status=400)

    # Filtra los abonos por nombre de cliente y los ordena por fecha
    abonos = Abono.objects.filter(
        cliente__nombre_cliente__icontains=query
    ).select_related('cliente', 'venta').order_by('-fecha')

    # Aplica la paginación a los resultados
    paginator = paginacion()
    result_page = paginator.paginate_queryset(abonos, request)
    serializer = AbonoReadSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)