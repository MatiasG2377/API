from rest_framework import serializers
from inventario.models import Categoria

# Este serializador convertirá los objetos Categoria a JSON y viceversa
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        # Estos campos no se podrán modificar en las peticiones PUT/PATCH
        read_only_fields = ['fecha_creacion_categoria', 'actualizacion_categoria']
    def validate_nombre_categoria(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")

        if Categoria.objects.filter(nombre_categoria__iexact=value.strip()).exists():
            raise serializers.ValidationError("Ya existe una categoría con ese nombre.")
        return value
