from enum import unique
from django.db import models
from django.core.exceptions import ValidationError  # si usas clean()

# Modelo Cliente: Almacena información básica de clientes
# - CI y nombre son campos obligatorios
# - Incluye índices para búsquedas eficientes por CI y nombre
class Cliente(models.Model):
    ci_cliente = models.TextField(null=False, unique=True)
    nombre_cliente = models.TextField(null=False)
    informacion_cliente = models.TextField(blank=True, null=True)
    correo_cliente = models.EmailField(unique=True, blank=True, null=True)
    telefono_cliente = models.TextField(blank=True, null=True)
    direccion_cliente = models.TextField(blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['ci_cliente'], name='idx_ci_cliente'),
            models.Index(fields=['nombre_cliente'], name='idx_nombre_cliente'),
        ]
    def __str__(self):
        return f"{self.id} | {self.nombre_cliente}"

# Modelo Paciente: Gestiona datos médicos y personales de pacientes
# - CI es único y obligatorio
# - Registra fecha automática al crear nuevo paciente
# - Incluye índices para búsquedas por CI, nombres y apellidos
class Paciente(models.Model):
    ci_paciente = models.CharField(max_length=20, unique=True)
    apellidos_paciente = models.CharField(max_length=255, blank=True, null=True)
    nombres_paciente = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    ocupacion_paciente = models.CharField(max_length=255, blank=True, null=True)
    direccion_paciente = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    telefono_paciente = models.CharField(max_length=20, blank=True, null=True)
    antecedentes_paciente = models.TextField(blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['ci_paciente'], name='idx_ci_paciente'),
            models.Index(fields=['apellidos_paciente'], name='idx_apellidos_paciente'),
            models.Index(fields=['nombres_paciente'], name='idx_nombres_paciente'),
        ]
    def __str__(self):
        nombres = self.nombres_paciente or ""
        apellidos = self.apellidos_paciente or ""
        nombre_completo = f"{nombres} {apellidos}".strip()
        return f"{self.id} | {nombre_completo or 'Paciente Sin Nombre'}"
