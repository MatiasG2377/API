from rest_framework import serializers
from inventario.models import FichaMedica, Paciente, Usuario
class PacienteResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'nombres_paciente', 'apellidos_paciente']

class UsuarioResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre_usuario', 'apellido_usuario']

class FichaMedicaReadSerializer(serializers.ModelSerializer):
    paciente = PacienteResumenSerializer(read_only=True)
    usuario = UsuarioResumenSerializer(read_only=True)

    class Meta:
        model = FichaMedica
        fields = '__all__'
        read_only_fields = ['id', 'fecha']

class FichaMedicaWriteSerializer(serializers.ModelSerializer):
    paciente = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all())
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = FichaMedica
        fields = '__all__'
        read_only_fields = ['id', 'fecha']
