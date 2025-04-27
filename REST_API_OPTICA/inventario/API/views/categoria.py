from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

from inventario.models import Categoria
from inventario.API.serializers.categoria import CategoriaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Categoria.objects.all().order_by('nombre_categoria')
    serializer_class = CategoriaSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_categorias_dinamico(request):
    """
    Buscador dinámico por nombre de categoría.
    Máximo 10 resultados.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    categorias = Categoria.objects.filter(
        nombre_categoria__icontains=query
    ).order_by('nombre_categoria')[:10]

    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)
