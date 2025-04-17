from rest_framework import serializers
from django.contrib.auth.models import User
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, Usuario, Sucursal, Kardex, FichaMedica, Abono, Paciente
from rest_framework.views import APIView


class categoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class proveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class productoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria_producto.nombre_categoria', read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'

class productoProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoProveedor
        fields = '__all__'

class clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ventaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class articuloVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloVenta
        fields = '__all__'


class movimientoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'

class loteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class sucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class FichaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaMedica
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

#! Manejo del login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Contraseña solo para escritura
        }

    def validate_password_field(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        # Validar la contraseña explícitamente
        self.validate_password_field(validated_data['password'])
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            self.validate_password_field(password)
            user.set_password(password)
            user.save()
        return user


# ---------------------------------- Serializador Kardex ----------------------------------------------


class KardexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kardex
        fields = '__all__'  # Incluye todos los campos del modelo

    def validate(self, data):
        """
        Validaciones personalizadas para asegurar la consistencia de los datos del Kardex.
        """
        if data['cantidad_kardex'] <= 0:
            raise serializers.ValidationError("La cantidad del movimiento debe ser mayor a cero.")
        if data['costo_unitario_kardex'] <= 0:
            raise serializers.ValidationError("El costo unitario debe ser mayor a cero.")
        if data['saldo_cantidad_kardex'] < 0:
            raise serializers.ValidationError("El saldo de cantidad no puede ser negativo.")
        return data


class UsuarioIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id']  # Solo necesitas el campo 'id'

# serializers.py

# Para GETs (mostrar con info anidada)
class ClienteAbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre_cliente']

class VentaAbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['id', 'total_venta']

class AbonoReadSerializer(serializers.ModelSerializer):
    cliente = ClienteAbonoSerializer(read_only=True)
    venta = VentaAbonoSerializer(read_only=True)

    class Meta:
        model = Abono
        fields = '__all__'


# Para POSTs (espera IDs)
class AbonoWriteSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    venta = serializers.PrimaryKeyRelatedField(queryset=Venta.objects.all())

    class Meta:
        model = Abono
        fields = '__all__'
