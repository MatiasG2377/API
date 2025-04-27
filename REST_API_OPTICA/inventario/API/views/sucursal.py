from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from inventario.models import Sucursal
from inventario.API.serializers.sucursal import SucursalSerializer


class SucursalPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


class SucursalViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Sucursal.objects.all().order_by('nombre_sucursal')
    serializer_class = SucursalSerializer
    pagination_class = SucursalPagination


@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_sucursales_dinamico(request):
    """
    Buscador dinámico por nombre parcial de sucursal.
    Devuelve máximo 10 resultados.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    sucursales = Sucursal.objects.filter(
        Q(nombre_sucursal__icontains=query)
    ).order_by('nombre_sucursal')[:10]

    serializer = SucursalSerializer(sucursales, many=True)
    return Response(serializer.data)
