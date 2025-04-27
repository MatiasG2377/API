from rest_framework import serializers
from inventario.models import Paciente
# Serializador para el modelo Paciente que maneja la conversión de datos
class PacienteSerializer(serializers.ModelSerializer):
    # Configuración del serializador
    class Meta:
        # Especifica el modelo a serializar
        model = Paciente
        # Incluye todos los campos del modelo
        fields = '__all__'
        # Define campos que solo son de lectura (no se pueden modificar)
        read_only_fields = ['id', 'fecha_registro']

    # Validación para el campo de cédula del paciente
    def validate_ci_paciente(self, value):
        if not value.strip():
            raise serializers.ValidationError("La cédula no puede estar vacía.")
        return value

    # Validación para el campo de nombres del paciente
    def validate_nombres_paciente(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    # Validación para el campo de apellidos del paciente
    def validate_apellidos_paciente(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido no puede estar vacío.")
        return value
