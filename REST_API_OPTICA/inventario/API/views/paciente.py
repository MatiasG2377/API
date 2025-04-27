from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from inventario.models import Paciente, FichaMedica
from inventario.API.serializers.paciente import PacienteSerializer
from inventario.API.serializers.ficha_medica import FichaMedicaReadSerializer


class PacientePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PacienteViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Paciente.objects.all().order_by('-fecha_registro')
    serializer_class = PacienteSerializer
    pagination_class = PacientePagination


@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_pacientes_dinamico(request):
    """
    Buscador dinámico por CI, nombres o apellidos del paciente.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    pacientes = Paciente.objects.filter(
        Q(ci_paciente__icontains=query) |
        Q(nombres_paciente__icontains=query) |
        Q(apellidos_paciente__icontains=query)
    ).order_by('-fecha_registro')[:10]

    serializer = PacienteSerializer(pacientes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_paciente_por_ci(request, ci):
    """
    Devuelve los datos del paciente con ese CI (exacto) y sus últimas 5 fichas médicas.
    """
    try:
        paciente = Paciente.objects.get(ci_paciente=ci)
        fichas = FichaMedica.objects.filter(paciente=paciente).order_by('-fecha')[:5]

        return Response({
            "paciente": PacienteSerializer(paciente).data,
            "historial_fichas": FichaMedicaReadSerializer(fichas, many=True).data
        })
    except Paciente.DoesNotExist:
        return Response({"detail": "Paciente no encontrado"}, status=404)
