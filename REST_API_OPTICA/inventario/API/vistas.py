from rest_framework import viewsets
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, Usuario, Sucursal, Kardex
from inventario.API.serializador import categoriaSerializer, productoSerializer, proveedorSerializer, productoProveedorSerializer, clienteSerializer, ventaSerializer, articuloVentaSerializer, movimientoInventarioSerializer, loteSerializer, UserSerializer, usuarioSerializer, sucursalSerializer, KardexSerializer, UsuarioIdSerializer
from django.contrib.auth.models import User
from django.db import models
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
    permission_classes = [AllowAny]

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
    
#------------------------------------------ Vistas para la generación de reportes --------------------------------
from django.db.models import Sum
from django.db.models.functions import TruncMonth


class ProductosBajoStockAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        productos_bajo_stock = Producto.objects.filter(cantidad_producto__lte=models.F('minimo_producto'))
        serializer = productoSerializer(productos_bajo_stock, many=True)
        return Response(serializer.data)

class VentasPorSucursalAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        ventas = Venta.objects.values('sucursal_venta__nombre_sucursal').annotate(total_ventas=Sum('total_venta'))
        return Response(ventas)

class HistorialKardexAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, producto_id):
        kardex_entries = Kardex.objects.filter(producto_kardex_id=producto_id).order_by('-fecha_kardex')
        serializer = KardexSerializer(kardex_entries, many=True)
        return Response(serializer.data)
    
class VentasPorMesAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        ventas_por_mes = (
            Venta.objects.annotate(mes=TruncMonth('fecha_venta'))
            .values('mes')
            .annotate(total_ventas=Sum('total_venta'))
            .order_by('mes')
        )
        return Response(ventas_por_mes)
    
class TopProductosVendidosAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        top_productos = (
            ArticuloVenta.objects.values('producto_articuloVenta__nombre_producto')
            .annotate(cantidad_vendida=Sum('cantidad_articuloVenta'))
            .order_by('-cantidad_vendida')[:5]
        )
        return Response(top_productos)
    
class IngresosPorSucursalAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        ingresos_por_sucursal = (
            Venta.objects.values('sucursal_venta__nombre_sucursal')
            .annotate(total_ingresos=Sum('total_venta'))
            .order_by('-total_ingresos')
        )
        return Response(ingresos_por_sucursal)

class MovimientosInventarioPorMesAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        movimientos_por_mes = (
            MovimientoInventario.objects.annotate(mes=TruncMonth('fecha_movimientoInventario'))
            .values('mes', 'tipo_movimientoInventario')
            .annotate(total_movimientos=Sum('cantidad_movimientoInventario'))
            .order_by('mes')
        )
        return Response(movimientos_por_mes)
    
class EvolucionStockProductoAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, producto_id):
        kardex_entries = (
            Kardex.objects.filter(producto_kardex_id=producto_id)
            .order_by('fecha_kardex')
            .values('fecha_kardex', 'saldo_cantidad_kardex')
        )
        return Response(kardex_entries)

# Generación de reportes gráficos
from rest_framework.parsers import JSONParser
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from django.apps import apps
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.exceptions import FieldDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound


class GenerateCustomChartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data

        # Obtener el modelo especificado
        model_name = data.get("model")
        try:
            Model = apps.get_model("inventario", model_name)  # Cambia 'inventario' por el nombre de tu aplicación
        except LookupError:
            return Response({"error": f"Modelo '{model_name}' no encontrado."}, status=400)

        # Aplicar filtros
        filters = data.get("filters", {})
        queryset = Model.objects.filter(**filters)

        # Obtener campos para los ejes
        x_field = data.get("xField")
        y_field = data.get("yField")
        if not x_field or not y_field:
            return Response({"error": "Los campos 'xField' y 'yField' son obligatorios."}, status=400)

        def resolve_field(queryset, field_name, model):
            field_parts = field_name.split('__')  # Separar niveles de relaciones
            for i in range(len(field_parts) - 1):
                # Excluir valores NULL en cada nivel de la relación
                related_field = '__'.join(field_parts[:i + 1]) + "__isnull"
                queryset = queryset.exclude(**{related_field: True})

            last_field = field_parts[-1]  # Último campo a resolver
            if len(field_parts) > 1:
                # Si hay relaciones anidadas
                data = queryset.values_list(field_name, flat=True)
            else:
                # Campo directo o FK en el nivel principal
                try:
                    field = model._meta.get_field(last_field)
                    if isinstance(field, ForeignKey):
                        # Obtener modelo relacionado
                        related_model = field.related_model

                        # Buscar un campo representativo (como nombre o descripción)
                        preferred_fields = ["nombre", "descripcion", "titulo"]
                        related_field_name = next(
                            (f"{last_field}__{field.name}" for field in related_model._meta.fields
                             if any(field.name.startswith(pref) for pref in preferred_fields)),
                            None
                        )

                        if related_field_name:
                            # Extraer datos del modelo relacionado
                            data = queryset.values_list(related_field_name, flat=True)
                        else:
                            # Si no hay un campo representativo, usar el id
                            data = queryset.values_list(last_field, flat=True)
                    else:
                        # Campo directo no relacionado
                        data = queryset.values_list(last_field, flat=True)
                except FieldDoesNotExist:
                    return Response({"error": f"Campo '{last_field}' no encontrado."}, status=400)

            # Reemplazar valores NULL por un valor predeterminado
            return [value if value is not None else "No cuenta con datos" for value in data]

        try:
            # Procesar datos para los campos X e Y
            x_data = resolve_field(queryset, x_field, Model)
            y_data = resolve_field(queryset, y_field, Model)

            # Filtrar combinaciones donde cualquiera sea NULL
            x_data, y_data = zip(*[
                (x, y) for x, y in zip(x_data, y_data) if x is not None and y is not None
            ])
        except ValueError:
            return Response({"error": "Los datos para el gráfico están vacíos o contienen valores nulos."}, status=400)

        # Validar datos no vacíos
        if not x_data or not y_data:
            return Response({"error": "No hay datos suficientes para generar el gráfico."}, status=400)

        # Generar el gráfico
        chart_type = data.get("chartType", "bar")
        plt.figure(figsize=(10, 6))
        if chart_type == "bar":
            plt.bar(x_data, y_data, color=data["options"].get("color", "#2196F3"))
        elif chart_type == "line":
            plt.plot(x_data, y_data, marker="o", color=data["options"].get("color", "#2196F3"))
        elif chart_type == "scatter":
            plt.scatter(x_data, y_data, color=data["options"].get("color", "#2196F3"))
        elif chart_type == "histogram":
            plt.hist(y_data, bins=10, edgecolor="black", color=data["options"].get("color", "#2196F3"))
            plt.xlabel(data["options"].get("xLabel", y_field))
            plt.ylabel("Frecuencia")
        else:
            return Response({"error": f"Tipo de gráfico '{chart_type}' no soportado."}, status=400)

        # Configurar títulos y etiquetas
        plt.title(data["options"].get("title", "Gráfico Personalizado"))
        plt.xlabel(data["options"].get("xLabel", x_field))
        plt.ylabel(data["options"].get("yLabel", y_field))

        # Rotar las etiquetas del eje X para que sean legibles
        plt.xticks(rotation=45, ha="right")  # Rotación de 45 grados, alineación a la derecha

        # Convertir el gráfico a Base64
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()

        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
        return Response({"image": img_base64})


class ModelFieldsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, model_name, *args, **kwargs):
        try:
            # Obtener el modelo dinámicamente
            Model = apps.get_model('inventario', model_name)  # Cambia 'inventario' por el nombre de tu aplicación
        except LookupError:
            raise NotFound(f"El modelo '{model_name}' no existe.")

        # Obtener los nombres de los campos del modelo
        fields = [field.name for field in Model._meta.fields]

        return Response({"fields": fields})


class ListModelsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Obtén todos los modelos registrados en la aplicación
        app_name = 'inventario'  # Cambia por el nombre de tu aplicación
        models = apps.get_app_config(app_name).get_models()

        # Devuelve solo los nombres de los modelos
        model_names = [model.__name__ for model in models]
        return Response({"models": model_names})


@api_view(['GET'])
def buscar_cliente_por_ci(request):
    ci = request.query_params.get('ci_cliente')
    if not ci:
        return Response({'error': 'Se requiere el parámetro ci_cliente'}, status=400)

    clientes = Cliente.objects.filter(ci_cliente=ci)
    serializer = clienteSerializer(clientes, many=True)
    return Response(serializer.data)
