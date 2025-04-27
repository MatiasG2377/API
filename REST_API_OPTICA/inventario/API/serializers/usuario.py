# Importación de módulos necesarios
from rest_framework import serializers
from inventario.models import Usuario

# Serializador principal para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        # Especifica el modelo a serializar
        model = Usuario
        # Incluye todos los campos del modelo
        fields = '__all__'
        # Campos que solo serán de lectura
        read_only_fields = ['id', 'fecha_creacion_usuario']

    # Método de validación para el nombre del usuario
    def validate_nombre_usuario(self, value):
        # Verifica que el nombre no esté vacío después de eliminar espacios
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    # Método de validación para el apellido del usuario
    def validate_apellido_usuario(self, value):
        # Verifica que el apellido no esté vacío después de eliminar espacios
        if not value.strip():
            raise serializers.ValidationError("El apellido no puede estar vacío.")
        return value


# Serializador simplificado que solo incluye el ID del usuario
class UsuarioIdSerializer(serializers.ModelSerializer):
    class Meta:
        # Especifica el modelo a serializar
        model = Usuario
        # Solo incluye el campo ID
        fields = ['id']

