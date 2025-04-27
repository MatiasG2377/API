from rest_framework import serializers
from inventario.models import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def validate_nombre_proveedor(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre del proveedor no puede estar vacío.")
        return value

    def validate_correo_proveedor(self, value):
        # Solo valida si se envía un correo (es opcional en tu modelo)
        if value and Proveedor.objects.filter(correo_proveedor=value).exists():
            raise serializers.ValidationError("Ya existe un proveedor con ese correo.")
        return value
