from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from inventario.models import Cliente
from inventario.API.serializers import ClienteSerializer


class ClientePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Cliente.objects.all().order_by('nombre_cliente')
    serializer_class = ClienteSerializer
    pagination_class = ClientePagination


@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_clientes_dinamico(request):
    """
    Buscador dinámico (autocomplete) por nombre o CI de cliente.
    Devuelve máx. 10 resultados.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    clientes = Cliente.objects.filter(
        Q(nombre_cliente__icontains=query) | Q(ci_cliente__icontains=query)
    ).order_by('nombre_cliente')[:10]

    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def cliente_por_ci_exacto(request):
    """
    Devuelve el cliente con CI exacto, para autocompletar formularios.
    """
    ci = request.query_params.get('ci', '').strip()
    if not ci:
        return Response({"detail": "Se requiere el parámetro 'ci'"}, status=400)

    try:
        cliente = Cliente.objects.get(ci_cliente=ci)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    except Cliente.DoesNotExist:
        return Response({"detail": "Cliente no encontrado"}, status=404)
