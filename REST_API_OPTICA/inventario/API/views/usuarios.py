from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

from inventario.models import Usuario
from inventario.API.serializers.usuario import UsuarioSerializer, UsuarioIdSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Usuario.objects.all().order_by('nombre_usuario')
    serializer_class = UsuarioSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_usuarios_dinamico(request):
    """
    Buscador dinámico por nombre o apellido del usuario.
    Devuelve máximo 10 resultados.
    """
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response([], status=200)

    usuarios = Usuario.objects.filter(
        Q(nombre_usuario__icontains=query) |
        Q(apellido_usuario__icontains=query)
    ).order_by('nombre_usuario')[:10]

    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_usuario_por_username(request):
    """
    Devuelve el ID del usuario buscando por su username exacto.
    """
    username = request.query_params.get('username', '').strip()
    if not username:
        return Response({"error": "El parámetro 'username' es requerido."}, status=400)

    try:
        usuario = Usuario.objects.get(username_usuario=username)
        serializer = UsuarioIdSerializer(usuario)
        return Response(serializer.data)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=404)
