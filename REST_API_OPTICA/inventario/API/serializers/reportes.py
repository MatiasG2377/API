from rest_framework import serializers

class EtiquetaValorSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.FloatField()
