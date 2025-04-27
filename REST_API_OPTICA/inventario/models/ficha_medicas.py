from django.db import models
from django.core.exceptions import ValidationError  # si usas clean()
from .clientes import Paciente 
from .base import Usuario

# Modelo para almacenar fichas médicas oftalmológicas
class FichaMedica(models.Model):
    # Campos básicos de la ficha
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)  # Relación con el paciente
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)    # Usuario que creó la ficha
    fecha = models.DateTimeField(auto_now_add=True)                               # Fecha automática de creación
    causa = models.TextField(blank=True, null=True)                               # Motivo de la consulta
    observaciones = models.TextField(blank=True, null=True)                       # Notas adicionales
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Altura del paciente
    material = models.CharField(max_length=100, blank=True, null=True)            # Material de los lentes

    # Campos para receta de distancia - Ojo Derecho (OD)
    rx_distancia_od_av = models.CharField(max_length=20, blank=True, null=True)
    rx_distancia_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_distancia_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_distancia_od_eje = models.IntegerField(blank=True, null=True)
    rx_distancia_od_dnp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Campos para receta de distancia - Ojo Izquierdo (OI)
    rx_distancia_oi_av = models.CharField(max_length=20, blank=True, null=True)
    rx_distancia_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_distancia_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_distancia_oi_eje = models.IntegerField(blank=True, null=True)
    rx_distancia_oi_dnp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Campos para adición - Ojo Derecho (OD)
    rx_add_od_av = models.CharField(max_length=20, blank=True, null=True)
    rx_add_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_add_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_add_od_eje = models.IntegerField(blank=True, null=True)
    rx_add_od_dnp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Campos para adición - Ojo Izquierdo (OI)
    rx_add_oi_av = models.CharField(max_length=20, blank=True, null=True)
    rx_add_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_add_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_add_oi_eje = models.IntegerField(blank=True, null=True)
    rx_add_oi_dnp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Campos para lectura - Ojo Derecho (OD)
    rx_lectura_od_av = models.CharField(max_length=20, blank=True, null=True)
    rx_lectura_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_lectura_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_lectura_od_eje = models.IntegerField(blank=True, null=True)

    # Campos para lectura - Ojo Izquierdo (OI)
    rx_lectura_oi_av = models.CharField(max_length=20, blank=True, null=True)
    rx_lectura_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_lectura_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_lectura_oi_eje = models.IntegerField(blank=True, null=True)

    # Campos para esquiascopia - Ojo Derecho (OD)
    esq_od_sc = models.CharField(max_length=20, blank=True, null=True)
    esq_od_cc = models.CharField(max_length=20, blank=True, null=True)
    esq_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    esq_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    esq_od_eje = models.IntegerField(blank=True, null=True)

    # Campos para esquiascopia - Ojo Izquierdo (OI)
    esq_oi_sc = models.CharField(max_length=20, blank=True, null=True)
    esq_oi_cc = models.CharField(max_length=20, blank=True, null=True)
    esq_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    esq_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    esq_oi_eje = models.IntegerField(blank=True, null=True)

    # Campos para receta subjetiva - Ojo Derecho (OD)
    rs_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_od_eje = models.IntegerField(blank=True, null=True)
    rs_od_correccion = models.CharField(max_length=100, blank=True, null=True)

    # Campos para receta subjetiva - Ojo Izquierdo (OI)
    rs_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_oi_eje = models.IntegerField(blank=True, null=True)
    rs_oi_correccion = models.CharField(max_length=100, blank=True, null=True)

    # Campos para receta subjetiva - Adición
    rs_add_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_add_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_add_eje = models.IntegerField(blank=True, null=True)
    rs_add_correccion = models.CharField(max_length=100, blank=True, null=True)

    # Configuración de índices para optimizar búsquedas
    class Meta:
        indexes = [
            models.Index(fields=['fecha'], name='idx_fecha_fichaMedica'),
            models.Index(fields=['paciente'], name='idx_paciente_fichaMedica'),
        ]

    # Representación en string del modelo
    def __str__(self):
        if self.paciente:
            nombres = self.paciente.nombres_paciente or ""
            apellidos = self.paciente.apellidos_paciente or ""
            paciente = f"{nombres} {apellidos}".strip()
        else:
            paciente = "Paciente Desconocido"
        return f"{self.id} | {paciente} | {self.fecha}"
