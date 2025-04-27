from rest_framework import serializers
from inventario.models import Cliente
# Serializador para el modelo Cliente que hereda de ModelSerializer
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        # Especifica el modelo a serializar
        model = Cliente
        # Incluye todos los campos del modelo
        fields = '__all__'
        # El campo ID será de solo lectura
        read_only_fields = ['id']

    # Método de validación para el campo cédula del cliente
    def validate_ci_cliente(self, value):
        if not value.strip():
            raise serializers.ValidationError("La cédula no puede estar vacía.")
        return value

    # Método de validación para el campo nombre del cliente
    def validate_nombre_cliente(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value
