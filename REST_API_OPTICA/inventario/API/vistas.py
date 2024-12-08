from rest_framework import viewsets
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, Usuario, Sucursal, Kardex
from inventario.API.serializador import categoriaSerializer, productoSerializer, proveedorSerializer, productoProveedorSerializer, clienteSerializer, ventaSerializer, articuloVentaSerializer, movimientoInventarioSerializer, loteSerializer, UserSerializer, usuarioSerializer, sucursalSerializer, KardexSerializer, UsuarioIdSerializer
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class usuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Usuario.objects.all()
    serializer_class = usuarioSerializer

class sucursalViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Sucursal.objects.all()
    serializer_class = sucursalSerializer

class categoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Categoria.objects.all()
    serializer_class = categoriaSerializer

class productoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Producto.objects.all()
    serializer_class = productoSerializer

class proveedorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Proveedor.objects.all()
    serializer_class = proveedorSerializer

class productoProveedorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ProductoProveedor.objects.all()
    serializer_class = productoProveedorSerializer

class clienteViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Cliente.objects.all()
    serializer_class = clienteSerializer

class ventaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Venta.objects.all()
    serializer_class = ventaSerializer

class articuloVentaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ArticuloVenta.objects.all()
    serializer_class = articuloVentaSerializer

class movimientoInventarioViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MovimientoInventario.objects.all()
    serializer_class = movimientoInventarioSerializer

class loteViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Lote.objects.all()
    serializer_class = loteSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class kardexViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Kardex.objects.all()
    serializer_class = KardexSerializer

class ProductoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        productos = Producto.objects.select_related('categoria_producto').all()
        serializer = productoSerializer(productos, many=True)
        return Response(serializer.data)

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permite acceso sin autenticación
    def post(self, request):
        print(f"Permisos actuales: {self.permission_classes}")  # Depuración
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Headers:", request.headers)
        print("Body:", request.data)

        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#----------------------------Filtrado       
class ProductoFiltradoPorCategoria(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categoria_id = request.query_params.get('categoria', None)
        if categoria_id:
            productos = Producto.objects.filter(categoria_producto_id=categoria_id)
        else:
            productos = Producto.objects.all()

        serializer = productoSerializer(productos, many=True)
        return Response(serializer.data)
    

class KardexPorProductoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, producto_id):
        try:
            # Filtrar movimientos del Kardex por el producto_id
            movimientos_kardex = Kardex.objects.filter(producto_kardex=producto_id).order_by('fecha_kardex')

            # Si no hay movimientos, devolver un error 404
            if not movimientos_kardex.exists():
                return Response({"detail": "No hay movimientos para este producto."}, status=status.HTTP_404_NOT_FOUND)

            # Serializar los datos y enviarlos como respuesta
            serializer = KardexSerializer(movimientos_kardex, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({"detail": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        

from rest_framework.decorators import api_view

@api_view(['GET'])
def obtener_id_usuario(request):
    username = request.query_params.get('username')  # Obtiene el parámetro de consulta
    if not username:
        return Response(
            {"error": "El parámetro 'username' es requerido."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Busca al usuario en la base de datos por el username
        usuario = Usuario.objects.get(username_usuario=username)  # Ajusta 'username_usuario' al nombre del campo en tu modelo
        serializer = UsuarioIdSerializer(usuario)  # Serializa el usuario
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response(
            {"error": "Usuario no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )