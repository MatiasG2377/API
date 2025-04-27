from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from django.db.models.functions import TruncMonth
from django.db.models import Sum

from inventario.models import MovimientoInventario
from inventario.API.serializers import MovimientoInventarioSerializer


class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MovimientoInventario.objects.select_related(
        'producto_movimientoInventario', 'usuario_movimientoInventario'
    ).order_by('-fecha_movimientoInventario')
    serializer_class = MovimientoInventarioSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_movimientos_dinamico(request):
    """
    Buscador dinámico de movimientos por nombre de producto.
    Devuelve máximo 10 resultados.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    movimientos = MovimientoInventario.objects.filter(
        producto_movimientoInventario__nombre_producto__icontains=query
    ).select_related('producto_movimientoInventario').order_by('-fecha_movimientoInventario')[:10]

    serializer = MovimientoInventarioSerializer(movimientos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def movimientos_agrupados_por_mes(request):
    """
    Reporte gráfico: Agrupa los movimientos por tipo y mes.
    """
    data = (
        MovimientoInventario.objects.annotate(mes=TruncMonth('fecha_movimientoInventario'))
        .values('mes', 'tipo_movimientoInventario')
        .annotate(total=Sum('cantidad_movimientoInventario'))
        .order_by('mes')
    )

    resultado = [
        {
            "label": f"{d['mes'].strftime('%B %Y')} - {d['tipo_movimientoInventario']}",
            "value": float(d["total"])
        }
        for d in data
    ]
    return Response(resultado)
