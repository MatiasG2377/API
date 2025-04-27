from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

from inventario.models import Proveedor
from inventario.API.serializers.proveedor import ProveedorSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Proveedor.objects.all().order_by('nombre_proveedor')
    serializer_class = ProveedorSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_proveedores_dinamico(request):
    """
    Buscador dinámico por nombre del proveedor o correo.
    Máximo 10 resultados.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    proveedores = Proveedor.objects.filter(
        Q(nombre_proveedor__icontains=query) |
        Q(correo_proveedor__icontains=query)
    ).order_by('nombre_proveedor')[:10]

    serializer = ProveedorSerializer(proveedores, many=True)
    return Response(serializer.data)
