from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db import models

from inventario.models import Producto, Venta, ArticuloVenta, MovimientoInventario, Kardex


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_ventas_por_mes(request):
    data = (
        Venta.objects
        .annotate(mes=TruncMonth('fecha_venta'))
        .values('mes')
        .annotate(total=Sum('total_venta'))
        .order_by('mes')
    )
    result = [{"label": d["mes"].strftime("%B %Y"), "value": float(d["total"])} for d in data]
    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_top_productos(request):
    data = (
        ArticuloVenta.objects
        .values('producto_articuloVenta__nombre_producto')
        .annotate(total=Sum('cantidad_articuloVenta'))
        .order_by('-total')[:5]
    )
    result = [{"label": d["producto_articuloVenta__nombre_producto"], "value": float(d["total"])} for d in data]
    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_ingresos_por_sucursal(request):
    data = (
        Venta.objects
        .values('sucursal_venta__nombre_sucursal')
        .annotate(total=Sum('total_venta'))
        .order_by('-total')
    )
    result = [{"label": d["sucursal_venta__nombre_sucursal"], "value": float(d["total"])} for d in data]
    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_movimientos_por_mes(request):
    data = (
        MovimientoInventario.objects
        .annotate(mes=TruncMonth('fecha_movimientoInventario'))
        .values('mes', 'tipo_movimientoInventario')
        .annotate(total=Sum('cantidad_movimientoInventario'))
        .order_by('mes')
    )
    result = [
        {
            "label": f"{d['mes'].strftime('%B %Y')} - {d['tipo_movimientoInventario']}",
            "value": float(d["total"])
        }
        for d in data
    ]
    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_evolucion_stock_producto(request, producto_id):
    data = Kardex.objects.filter(producto_kardex_id=producto_id).order_by('fecha_kardex').values(
        'fecha_kardex', 'saldo_cantidad_kardex'
    )
    result = [{"label": d["fecha_kardex"].strftime("%d-%m-%Y"), "value": float(d["saldo_cantidad_kardex"])} for d in data]
    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_productos_bajo_stock(request):
    data = Producto.objects.filter(controla_stock=True, cantidad_producto__lte=models.F('minimo_producto')).values(
        'nombre_producto', 'cantidad_producto'
    )
    result = [{"label": d["nombre_producto"], "value": float(d["cantidad_producto"])} for d in data]
    return Response(result)
