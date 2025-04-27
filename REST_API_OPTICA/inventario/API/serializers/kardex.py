from inventario.models import Producto

# Serializador para mostrar información resumida de productos
from rest_framework import serializers
from inventario.models import Kardex

class ProductoResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre_producto']

# Serializador para lectura de kardex que incluye información del producto
class KardexReadSerializer(serializers.ModelSerializer):
    producto_kardex = ProductoResumenSerializer(read_only=True)

    class Meta:
        model = Kardex
        fields = '__all__'

# Serializador para escritura de kardex con validaciones de datos
class KardexWriteSerializer(serializers.ModelSerializer):
    producto_kardex = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = Kardex
        fields = '__all__'
        read_only_fields = ['id', 'fecha_kardex']

    # Validaciones para los campos numéricos del kardex
    def validate(self, data):
        errors = {}

        if data['cantidad_kardex'] <= 0:
            errors['cantidad_kardex'] = "La cantidad del movimiento debe ser mayor a cero."
        if data['costo_unitario_kardex'] <= 0:
            errors['costo_unitario_kardex'] = "El costo unitario debe ser mayor a cero."
        if data['tipo_kardex'] == 'Salida' and data['saldo_cantidad_kardex'] < data['cantidad_kardex']:
            errors['saldo_cantidad_kardex'] = "Saldo insuficiente para realizar esta salida."
        if errors:
            raise serializers.ValidationError(errors)
        return data