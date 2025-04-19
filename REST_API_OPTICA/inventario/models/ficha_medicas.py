from django.db import models
from .clientes import Paciente
from .base import Usuario

class FichaMedica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    causa = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)

    rx_distancia_od_av = models.CharField(max_length=20, blank=True, null=True)
    rx_distancia_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_distancia_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_distancia_od_eje = models.IntegerField(blank=True, null=True)
    rx_distancia_od_dnp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    rx_distancia_oi_av = models.CharField(max_length=20, blank=True, null=True)
    rx_distancia_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_distancia_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_distancia_oi_eje = models.IntegerField(blank=True, null=True)
    rx_distancia_oi_dnp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    rx_add_od_av = models.CharField(max_length=20, blank=True, null=True)
    rx_add_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_add_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_add_od_eje = models.IntegerField(blank=True, null=True)
    rx_add_od_dnp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    rx_add_oi_av = models.CharField(max_length=20, blank=True, null=True)
    rx_add_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_add_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_add_oi_eje = models.IntegerField(blank=True, null=True)
    rx_add_oi_dnp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    rx_lectura_od_av = models.CharField(max_length=20, blank=True, null=True)
    rx_lectura_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_lectura_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_lectura_od_eje = models.IntegerField(blank=True, null=True)

    rx_lectura_oi_av = models.CharField(max_length=20, blank=True, null=True)
    rx_lectura_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_lectura_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rx_lectura_oi_eje = models.IntegerField(blank=True, null=True)

    esq_od_sc = models.CharField(max_length=20, blank=True, null=True)
    esq_od_cc = models.CharField(max_length=20, blank=True, null=True)
    esq_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    esq_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    esq_od_eje = models.IntegerField(blank=True, null=True)

    esq_oi_sc = models.CharField(max_length=20, blank=True, null=True)
    esq_oi_cc = models.CharField(max_length=20, blank=True, null=True)
    esq_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    esq_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    esq_oi_eje = models.IntegerField(blank=True, null=True)

    rs_od_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_od_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_od_eje = models.IntegerField(blank=True, null=True)
    rs_od_correccion = models.CharField(max_length=100, blank=True, null=True)

    rs_oi_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_oi_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_oi_eje = models.IntegerField(blank=True, null=True)
    rs_oi_correccion = models.CharField(max_length=100, blank=True, null=True)

    rs_add_esfera = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_add_cilindro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rs_add_eje = models.IntegerField(blank=True, null=True)
    rs_add_correccion = models.CharField(max_length=100, blank=True, null=True)
