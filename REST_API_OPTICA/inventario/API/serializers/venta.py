# Importamos los módulos necesarios de rest_framework y los modelos que vamos a serializar
from rest_framework import serializers
from inventario.models import Venta, ArticuloVenta

# Serializador para el modelo Venta
# Esta clase permite convertir objetos Venta a JSON y viceversa
class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        # Especificamos el modelo a serializar
        model = Venta
        # Incluimos todos los campos del modelo
        fields = '__all__'
        # Definimos campos que solo serán de lectura (no se pueden modificar)
        read_only_fields = ['id', 'fecha_venta', 'total_venta']


# Serializador para el modelo ArticuloVenta
# Esta clase permite convertir objetos ArticuloVenta a JSON y viceversa
class ArticuloVentaSerializer(serializers.ModelSerializer):
    class Meta:
        # Especificamos el modelo a serializar
        model = ArticuloVenta
        # Incluimos todos los campos del modelo
        fields = '__all__'

    # Método de validación para la cantidad de artículos en la venta
    # Verifica que la cantidad sea mayor a cero
    def validate_cantidad_articuloVenta(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value

    # Método de validación para el precio de venta al público
    # Verifica que el precio no sea negativo o cero
    def validate_pvp_articuloVenta(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio no puede ser cero o negativo.")
        return value
