from rest_framework import serializers
from inventario.models import Abono, Cliente, Venta

# Serializador para mostrar información básica del cliente en los abonos
class ClienteAbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre_cliente']

# Serializador para mostrar información básica de la venta en los abonos
class VentaAbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['id', 'total_venta']

# Serializador para lectura de abonos que incluye información detallada del cliente y la venta
class AbonoReadSerializer(serializers.ModelSerializer):
    cliente = ClienteAbonoSerializer(read_only=True)
    venta = VentaAbonoSerializer(read_only=True)

    class Meta:
        model = Abono
        fields = '__all__'

# Serializador para escritura de abonos que solo requiere los IDs del cliente y la venta
class AbonoWriteSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    venta = serializers.PrimaryKeyRelatedField(queryset=Venta.objects.all())

    class Meta:
        model = Abono
        fields = '__all__'
        read_only_fields = ['fecha']
    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value
