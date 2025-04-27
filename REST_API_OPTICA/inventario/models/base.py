from django.db import models
from django.core.exceptions import ValidationError  # si usas clean()

ROLES_USUARIO_CHOICES = [
    ('Administrador', 'Administrador'),
    ('Gerente', 'Gerente'),
    ('Usuario', 'Usuario'),
]

class Sucursal(models.Model):
    nombre_sucursal = models.TextField(null=False)
    direccion_sucursal = models.TextField(null=True)
    telefono_sucursal = models.TextField(blank=True, null=True)
    activo_sucursal = models.BooleanField(default=True)
    fecha_creacion_sucursal = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['nombre_sucursal'], name='idx_nombre_sucursal'),
        ]
    def __str__(self):
        return f"{self.id} | {self.nombre_sucursal}"

class Usuario(models.Model):
    nombre_usuario = models.TextField(null=False)
    apellido_usuario = models.TextField(null=False)
    email_usuario = models.EmailField(unique=True, null=False)
    telefono_usuario = models.TextField(blank=True, null=True)
    rol_usuario = models.CharField(max_length=20, choices=ROLES_USUARIO_CHOICES, default='Usuario')
    sucursal_usuario = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion_usuario = models.DateTimeField(auto_now_add=True)
    activo_usuario = models.BooleanField(default=True)
    username_usuario = models.CharField(max_length=150, unique=True, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email_usuario'], name='idx_email_usuario'),
            models.Index(fields=['nombre_usuario'], name='idx_nombre_usuario'),
            models.Index(fields=['apellido_usuario'], name='idx_apellido_usuario'),
        ]

    def __str__(self):
        return f"{self.id} | {self.nombre_usuario} {self.apellido_usuario}"
