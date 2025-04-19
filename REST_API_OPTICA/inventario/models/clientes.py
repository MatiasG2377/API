from django.db import models

class Cliente(models.Model):
    ci_cliente = models.TextField(null=False)
    nombre_cliente = models.TextField(null=False)
    informacion_cliente = models.TextField(blank=True, null=True)
    correo_cliente = models.EmailField(unique=True, blank=True, null=True)
    telefono_cliente = models.TextField(blank=True, null=True)
    direccion_cliente = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_cliente

class Paciente(models.Model):
    ci_paciente = models.CharField(max_length=20, unique=True)
    apellidos = models.CharField(max_length=255, blank=True, null=True)
    nombres = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    ocupacion = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    telefono_celular = models.CharField(max_length=20, blank=True, null=True)
    antecedentes = models.TextField(blank=True, null=True)
