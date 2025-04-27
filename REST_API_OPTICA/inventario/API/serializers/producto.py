from rest_framework import serializers
from inventario.models import Producto

# Serializador para el modelo Producto que maneja la conversión de datos
class ProductoSerializer(serializers.ModelSerializer):
    # Campo adicional para mostrar el nombre de la categoría
    categoria_nombre = serializers.CharField(source='categoria_producto.nombre_categoria', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ['id', 'fecha_ingreso_producto']  # ← ya no incluimos 'ultima_venta_producto'

    # Validación del precio de venta al público
    def validate_pvp_producto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio de venta debe ser mayor a cero.")
        return value

    # Validación del costo del producto
    def validate_costo_producto(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("El costo no puede ser negativo.")
        return value

    # Validación de la cantidad en inventario
    def validate_cantidad_producto(self, value):
        if self.initial_data.get('controla_stock') == 'true' and value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa.")
        return value

    # Validación cruzada entre stock mínimo y máximo
    def validate(self, data):
        min_stock = data.get('minimo_producto')
        max_stock = data.get('maximo_producto')

        if min_stock is not None and max_stock is not None and min_stock > max_stock:
            raise serializers.ValidationError("El stock mínimo no puede ser mayor que el stock máximo.")
        return data
