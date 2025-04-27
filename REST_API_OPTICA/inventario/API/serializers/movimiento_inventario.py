from rest_framework import serializers
from inventario.models import MovimientoInventario


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='producto_movimientoInventario.nombre_producto',
        read_only=True
    )
    usuario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = MovimientoInventario
        fields = '__all__'
        read_only_fields = ['id', 'fecha_movimientoInventario']

    def get_usuario_nombre(self, obj):
        if obj.usuario_movimientoInventario:
            return f"{obj.usuario_movimientoInventario.nombre_usuario} {obj.usuario_movimientoInventario.apellido_usuario}"
        return "—"

    def validate_cantidad_movimientoInventario(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value
