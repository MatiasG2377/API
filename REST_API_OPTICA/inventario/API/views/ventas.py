from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth

from inventario.models import Venta, ArticuloVenta
from inventario.API.serializers.venta import VentaSerializer, ArticuloVentaSerializer


class VentaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Venta.objects.select_related('cliente_venta', 'usuario_venta', 'sucursal_venta').order_by('-fecha_venta')
    serializer_class = VentaSerializer


class ArticuloVentaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ArticuloVenta.objects.select_related('venta_articuloVenta', 'producto_articuloVenta')
    serializer_class = ArticuloVentaSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_ventas_por_cliente(request):
    """
    Devuelve ventas filtradas por nombre parcial del cliente.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    ventas = Venta.objects.filter(
        cliente_venta__nombre_cliente__icontains=query
    ).select_related('cliente_venta', 'usuario_venta', 'sucursal_venta').order_by('-fecha_venta')[:10]

    serializer = VentaSerializer(ventas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def ventas_agrupadas_por_mes(request):
    """
    Devuelve el total de ventas agrupado por mes (para gráfico).
    """
    ventas = (
        Venta.objects.annotate(mes=TruncMonth('fecha_venta'))
        .values('mes')
        .annotate(total_ventas=Sum('total_venta'))
        .order_by('mes')
    )

    data = [
        {"label": venta["mes"].strftime("%B %Y"), "value": float(venta["total_ventas"])}
        for venta in ventas
    ]
    return Response(data)
