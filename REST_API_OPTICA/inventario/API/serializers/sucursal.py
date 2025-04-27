# Importamos los módulos necesarios de Django REST framework y nuestro modelo
from rest_framework import serializers
from inventario.models import Sucursal

# Definimos el serializador para el modelo Sucursal
class SucursalSerializer(serializers.ModelSerializer):
    # Configuración del serializador
    class Meta:
        # Especificamos el modelo a serializar
        model = Sucursal
        # Incluimos todos los campos del modelo
        fields = '__all__'
        # Definimos campos que solo serán de lectura (no se pueden modificar)
        read_only_fields = ['id', 'fecha_creacion_sucursal']

    # Método de validación personalizado para el campo nombre_sucursal
    def validate_nombre_sucursal(self, value):
        # Verificamos que el nombre no esté vacío después de eliminar espacios
        if not value.strip():
            raise serializers.ValidationError("El nombre de la sucursal no puede estar vacío.")
        return value
