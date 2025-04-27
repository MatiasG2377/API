from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from django.db.models.functions import TruncMonth

from inventario.models import Kardex
from inventario.API.serializers.kardex import KardexReadSerializer, KardexWriteSerializer


class KardexViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Kardex.objects.select_related('producto_kardex').order_by('-fecha_kardex')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return KardexWriteSerializer
        return KardexReadSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def historial_kardex_por_producto(request, producto_id):
    """
    Devuelve el historial completo de movimientos de un producto específico.
    """
    movimientos = Kardex.objects.filter(producto_kardex_id=producto_id).order_by('-fecha_kardex')
    serializer = KardexReadSerializer(movimientos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def evolucion_stock_producto(request, producto_id):
    """
    Devuelve la evolución cronológica del stock para un producto específico.
    Ideal para gráficas de línea.
    """
    movimientos = (
        Kardex.objects.filter(producto_kardex_id=producto_id)
        .order_by('fecha_kardex')
        .values('fecha_kardex', 'saldo_cantidad_kardex')
    )
    return Response(list(movimientos))
