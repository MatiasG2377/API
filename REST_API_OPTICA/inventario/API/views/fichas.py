# Importaciones necesarias de Django REST framework y Django
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Importación de modelos y serializadores
from inventario.models import FichaMedica, Paciente
from inventario.API.serializers import (
    FichaMedicaReadSerializer,
    FichaMedicaWriteSerializer,
    PacienteSerializer
)

# Clase para manejar la paginación de fichas médicas
# Define un tamaño de página de 10 elementos con un máximo de 100
class FichaMedicaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ViewSet principal para el manejo de fichas médicas
# Permite operaciones CRUD completas sobre las fichas médicas
class FichaMedicaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = FichaMedica.objects.select_related('paciente', 'usuario').order_by('-fecha')
    pagination_class = FichaMedicaPagination

    # Método para determinar qué serializador usar según el tipo de petición
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return FichaMedicaWriteSerializer
        return FichaMedicaReadSerializer


# Vista para búsqueda dinámica de fichas médicas
# Permite buscar por nombre o CI del paciente
@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_fichas_dinamico(request):
    """
    Buscador dinámico por nombre o CI del paciente. Máximo 10 resultados.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    # Búsqueda de pacientes que coincidan con el criterio y tengan ficha médica
    pacientes_con_ficha = Paciente.objects.filter(
        Q(nombres_paciente__icontains=query) | Q(ci_paciente__icontains=query)
    ).filter(fichamedica__isnull=False).distinct()[:10]

    serializer = PacienteSerializer(pacientes_con_ficha, many=True)
    return Response(serializer.data)


# Vista para obtener todas las fichas médicas de un paciente específico
@api_view(['GET'])
@permission_classes([AllowAny])
def fichas_por_paciente(request):
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response({"detail": "Se requiere el parámetro 'q'"}, status=400)

    # Búsqueda de fichas médicas por nombre o CI del paciente
    fichas = FichaMedica.objects.filter(
        Q(paciente__nombres_paciente__icontains=query) |
        Q(paciente__ci_paciente__icontains=query)
    ).select_related('paciente', 'usuario').order_by('-fecha')

    # Paginación de resultados
    paginator = FichaMedicaPagination()
    result_page = paginator.paginate_queryset(fichas, request)
    serializer = FichaMedicaReadSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
